from __future__ import annotations

import re
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


def check_repository(url: str) -> str:
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

    return "found" if 200 <= status < 300 else "not found"
