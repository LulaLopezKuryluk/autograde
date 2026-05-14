"""Repository validator module."""

import tempfile
import shutil
from pathlib import Path
from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError


class RepositoryValidator:
    """Validates GitHub repositories based on specified conditions."""

    def __init__(self, repo_url: str):
        """Initialize validator with repository URL."""
        self.repo_url = repo_url
        self.temp_dir = None
        self.repo = None

    def validate(self) -> dict:
        """
        Validate the repository against all conditions.
        
        Returns:
            dict: Dictionary with validation results and details
        """
        results = {
            "url": self.repo_url,
            "is_git_repository": False,
            "has_main_branch": False,
            "has_feature_branch": False,
            "has_file_txt_on_main": False,
            "all_conditions_met": False,
            "errors": []
        }

        try:
            # Clone the repository
            self.temp_dir = tempfile.mkdtemp()
            self.repo = Repo.clone_from(self.repo_url, self.temp_dir)
            
            # Check 1: Is it a git repository
            results["is_git_repository"] = True
            
            # Check 2: Has main branch
            results["has_main_branch"] = self._check_main_branch()
            
            # Check 3: Has feature branch in remote
            results["has_feature_branch"] = self._check_feature_branch()
            
            # Check 4: Has file.txt on main branch
            results["has_file_txt_on_main"] = self._check_file_txt_on_main()
            
            # All conditions met
            results["all_conditions_met"] = all([
                results["is_git_repository"],
                results["has_main_branch"],
                results["has_feature_branch"],
                results["has_file_txt_on_main"]
            ])

        except InvalidGitRepositoryError as e:
            results["errors"].append(f"Not a valid git repository: {str(e)}")
        except GitCommandError as e:
            results["errors"].append(f"Git command error: {str(e)}")
        except Exception as e:
            results["errors"].append(f"Error: {str(e)}")
        finally:
            # Clean up temporary directory
            self._cleanup()

        return results

    def _check_main_branch(self) -> bool:
        """Check if main branch exists in remote."""
        try:
            remote_refs = self.repo.remotes.origin.refs
            for ref in remote_refs:
                if ref.remote_head == "main":
                    return True
            return False
        except Exception:
            return False

    def _check_feature_branch(self) -> bool:
        """Check if feature branch exists in remote."""
        try:
            remote_refs = self.repo.remotes.origin.refs
            for ref in remote_refs:
                if ref.remote_head == "feature":
                    return True
            return False
        except Exception:
            return False

    def _check_file_txt_on_main(self) -> bool:
        """Check if file.txt exists on main branch."""
        try:
            if not self._check_main_branch():
                return False
            
            # Checkout main branch
            self.repo.heads.main.checkout()
            
            # Check if file.txt exists
            file_path = Path(self.temp_dir) / "file.txt"
            return file_path.exists()
        except Exception:
            return False

    def _cleanup(self):
        """Clean up temporary directory."""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
