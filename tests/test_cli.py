"""Tests for the CLI module."""

import pytest
from unittest.mock import patch, MagicMock
from autograde.cli import main, print_results


def test_main_with_invalid_url(capsys):
    """Test main function with invalid URL."""
    with patch("sys.argv", ["autograde", "invalid-url"]):
        exit_code = main()
    
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "invalid-url" in captured.out


def test_main_with_json_output(capsys):
    """Test main function with JSON output flag."""
    with patch("sys.argv", ["autograde", "invalid-url", "--json"]):
        exit_code = main()
    
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "invalid-url" in captured.out
    
    # Check if output looks like JSON
    import json
    try:
        json.loads(captured.out)
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")


def test_print_results_all_met(capsys):
    """Test print_results when all conditions are met."""
    results = {
        "url": "https://github.com/test/repo.git",
        "is_git_repository": True,
        "has_main_branch": True,
        "has_feature_branch": True,
        "has_file_txt_on_main": True,
        "all_conditions_met": True,
        "errors": []
    }
    
    print_results(results)
    captured = capsys.readouterr()
    
    assert "https://github.com/test/repo.git" in captured.out
    assert "All Conditions Met:       True" in captured.out
    assert "Is Git Repository:        True" in captured.out
    assert "Has Main Branch:          True" in captured.out
    assert "Has Feature Branch:       True" in captured.out
    assert "Has file.txt on Main:     True" in captured.out


def test_print_results_some_failures(capsys):
    """Test print_results when some conditions fail."""
    results = {
        "url": "https://github.com/test/repo.git",
        "is_git_repository": True,
        "has_main_branch": False,
        "has_feature_branch": True,
        "has_file_txt_on_main": False,
        "all_conditions_met": False,
        "errors": []
    }
    
    print_results(results)
    captured = capsys.readouterr()
    
    assert "All Conditions Met:       False" in captured.out
    assert "Has Main Branch:          False" in captured.out
    assert "Has file.txt on Main:     False" in captured.out


def test_print_results_with_errors(capsys):
    """Test print_results with error messages."""
    results = {
        "url": "invalid-url",
        "is_git_repository": False,
        "has_main_branch": False,
        "has_feature_branch": False,
        "has_file_txt_on_main": False,
        "all_conditions_met": False,
        "errors": ["Error message 1", "Error message 2"]
    }
    
    print_results(results)
    captured = capsys.readouterr()
    
    assert "Errors:" in captured.out
    assert "Error message 1" in captured.out
    assert "Error message 2" in captured.out
