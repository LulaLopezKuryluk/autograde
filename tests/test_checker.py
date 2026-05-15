import pytest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError
from urllib.request import Request

from github_checker.checker import check_repository, is_valid_github_repo_url


class DummyResponse:
    def __init__(self, status: int):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/python/cpython",
        "https://github.com/python/cpython/",
        "https://github.com/python/cpython.git",
    ],
)
def test_is_valid_github_repo_url_accepts_valid_urls(url):
    assert is_valid_github_repo_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "http://github.com/python/cpython",
        "https://gitlab.com/python/cpython",
        "https://github.com/python",
        "https://github.com/python/cpython/issues",
        "https://github.com/python/cpython/tree/main",
        "not a url",
        "",
        "   ",
    ],
)
def test_is_valid_github_repo_url_rejects_invalid_urls(url):
    assert not is_valid_github_repo_url(url)


@patch("github_checker.checker.urlopen")
def test_check_repository_returns_found_when_repo_exists(mock_urlopen):
    mock_urlopen.return_value = DummyResponse(status=200)

    assert check_repository("https://github.com/python/cpython") == "found"
    mock_urlopen.assert_called_once()


@patch("github_checker.checker.urlopen")
def test_check_repository_returns_not_found_on_404(mock_urlopen):
    mock_urlopen.side_effect = HTTPError(
        url="https://github.com/python/does-not-exist",
        code=404,
        msg="Not Found",
        hdrs=None,
        fp=None,
    )

    assert check_repository("https://github.com/python/does-not-exist") == "not found"


@patch("github_checker.checker.urlopen")
def test_check_repository_returns_not_found_on_client_error(mock_urlopen):
    mock_urlopen.side_effect = HTTPError(
        url="https://github.com/python/does-not-exist",
        code=410,
        msg="Gone",
        hdrs=None,
        fp=None,
    )

    assert check_repository("https://github.com/python/does-not-exist") == "not found"


@patch("github_checker.checker.urlopen")
def test_check_repository_falls_back_to_get_on_head_not_allowed(mock_urlopen):
    error = HTTPError(
        url="https://github.com/python/cpython",
        code=405,
        msg="Method Not Allowed",
        hdrs=None,
        fp=None,
    )

    mock_urlopen.side_effect = [error, DummyResponse(status=200)]

    assert check_repository("https://github.com/python/cpython") == "found"
    assert mock_urlopen.call_count == 2


def test_check_repository_returns_invalid_url_for_non_github_url():
    assert check_repository("https://example.com/python/cpython") == "invalid URL"


@patch("github_checker.checker.urlopen")
def test_check_repository_raises_connection_error_for_network_issues(mock_urlopen):
    mock_urlopen.side_effect = URLError("No route to host")

    with pytest.raises(ConnectionError):
        check_repository("https://github.com/python/cpython")
