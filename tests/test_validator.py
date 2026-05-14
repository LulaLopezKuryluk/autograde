"""Tests for the repository validator."""

import pytest
import tempfile
import shutil
from pathlib import Path
from git import Repo
from autograde.validator import RepositoryValidator


@pytest.fixture
def temp_repo():
    """Create a temporary git repository for testing."""
    temp_dir = tempfile.mkdtemp()
    repo = Repo.init(temp_dir)
    
    yield temp_dir, repo
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def valid_test_repo(temp_repo):
    """Create a valid test repository that meets all conditions."""
    temp_dir, repo = temp_repo
    
    # Create file.txt
    file_path = Path(temp_dir) / "file.txt"
    file_path.write_text("test content")
    
    # Configure user
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Test User")
        git_config.set_value("user", "email", "test@example.com")
    
    # Add and commit file.txt
    repo.index.add(["file.txt"])
    repo.index.commit("Initial commit with file.txt")
    
    # Create main branch (rename master to main if needed)
    try:
        repo.heads.master.rename("main")
    except Exception:
        pass
    
    # Create feature branch
    repo.create_head("feature")
    
    yield temp_dir, repo


def test_validator_with_invalid_url():
    """Test validator with invalid repository URL."""
    validator = RepositoryValidator("not-a-valid-url")
    results = validator.validate()
    
    assert results["is_git_repository"] is False
    assert results["all_conditions_met"] is False
    assert len(results["errors"]) > 0


def test_validator_initialization():
    """Test validator initialization."""
    url = "https://github.com/user/repo.git"
    validator = RepositoryValidator(url)
    
    assert validator.repo_url == url
    assert validator.temp_dir is None
    assert validator.repo is None


def test_results_structure():
    """Test that validation results have the correct structure."""
    validator = RepositoryValidator("invalid-url")
    results = validator.validate()
    
    required_keys = {
        "url",
        "is_git_repository",
        "has_main_branch",
        "has_feature_branch",
        "has_file_txt_on_main",
        "all_conditions_met",
        "errors"
    }
    
    assert all(key in results for key in required_keys)
    assert isinstance(results["errors"], list)
    assert isinstance(results["is_git_repository"], bool)
    assert isinstance(results["has_main_branch"], bool)
    assert isinstance(results["has_feature_branch"], bool)
    assert isinstance(results["has_file_txt_on_main"], bool)
    assert isinstance(results["all_conditions_met"], bool)


def test_check_main_branch_not_exists(temp_repo):
    """Test checking for main branch when it doesn't exist."""
    temp_dir, repo = temp_repo
    
    # Configure user
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Test User")
        git_config.set_value("user", "email", "test@example.com")
    
    # Create initial commit
    (Path(temp_dir) / "README.md").write_text("test")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    
    validator = RepositoryValidator(temp_dir)
    assert validator._check_main_branch() is False


def test_check_feature_branch_not_exists(temp_repo):
    """Test checking for feature branch when it doesn't exist."""
    temp_dir, repo = temp_repo
    
    # Configure user
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Test User")
        git_config.set_value("user", "email", "test@example.com")
    
    # Create initial commit and main branch
    (Path(temp_dir) / "README.md").write_text("test")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    
    try:
        repo.heads.master.rename("main")
    except Exception:
        pass
    
    validator = RepositoryValidator(temp_dir)
    assert validator._check_feature_branch() is False


def test_check_file_txt_not_exists(temp_repo):
    """Test checking for file.txt when it doesn't exist."""
    temp_dir, repo = temp_repo
    
    # Configure user
    with repo.config_writer() as git_config:
        git_config.set_value("user", "name", "Test User")
        git_config.set_value("user", "email", "test@example.com")
    
    # Create initial commit without file.txt
    (Path(temp_dir) / "README.md").write_text("test")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    
    try:
        repo.heads.master.rename("main")
    except Exception:
        pass
    
    validator = RepositoryValidator(temp_dir)
    validator.repo = repo
    validator.temp_dir = temp_dir
    
    assert validator._check_file_txt_on_main() is False
