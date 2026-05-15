from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path
from shutil import rmtree
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

GITHUB_HOST = "github.com"
REPO_PATH_RE = re.compile(r"^/([^/]+)/([^/]+?)(?:\.git)?/?$")
USER_AGENT = "github-checker/0.1"


def is_valid_github_repo_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    url = url.strip()
    if not url:
        return False

    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        return False
    if parsed.netloc.lower() != GITHUB_HOST:
        return False
    if not REPO_PATH_RE.fullmatch(parsed.path):
        return False

    return True


def _send_head_request(url: str) -> int:
    request = Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=10) as response:
        return response.status


def _send_get_request(url: str) -> int:
    request = Request(url, method="GET", headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=10) as response:
        return response.status


def _clone_and_run_tests(url: str) -> str:
    """Clone repository and run tests, returning test results."""
    temp_dir = tempfile.mkdtemp(prefix="github_checker_")
    try:
        # Clone the repository
        result = subprocess.run(
            ["git", "clone", url, temp_dir],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return f"failed to clone: {result.stderr}"

        # Prepare environment for subprocess (remove VIRTUAL_ENV to avoid conflicts)
        import os
        env = os.environ.copy()
        env.pop("VIRTUAL_ENV", None)
        
        # First, sync dependencies with uv
        sync_result = subprocess.run(
            ["uv", "sync"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )
        
        if sync_result.returncode != 0:
            # If uv sync fails, try just running pytest anyway (might still work)
            pass
        
        # Then run tests with uv
        result = subprocess.run(
            ["uv", "run", "pytest", "--tb=short", "-q"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )
        
        output = result.stdout + result.stderr
        
        if result.returncode == 0:
            # Count passed tests
            import re
            passed_match = re.search(r"(\d+) passed", output)
            if passed_match:
                return f"tests passed: {passed_match.group(1)} tests"
            return "tests passed"
        else:
            # Check if pytest is not installed or no tests
            if "no tests ran" in output.lower() or "no module named pytest" in output.lower():
                return f"no tests found or pytest not available"
            if "No module named" in output:
                return f"dependencies not available"
            return f"tests failed"
    except subprocess.TimeoutExpired:
        return "timeout: test execution took too long"
    except FileNotFoundError:
        return "error: git or uv not found in PATH"
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        # Cleanup temp directory
        try:
            rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


def check_repository(url: str, run_tests: bool = False) -> str:
    if not is_valid_github_repo_url(url):
        return "invalid URL"

    normalized = url.strip()

    try:
        status = _send_head_request(normalized)
    except HTTPError as error:
        if error.code == 405:
            status = _send_get_request(normalized)
        elif error.code == 404:
            return "not found"
        elif 400 <= error.code < 500:
            return "not found"
        else:
            raise
    except URLError as error:
        raise ConnectionError(f"Network error while checking repository: {error}") from error

    if not (200 <= status < 300):
        return "not found"

    if run_tests:
        return _clone_and_run_tests(normalized)
    
    return "found"
