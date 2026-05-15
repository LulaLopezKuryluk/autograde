# GitHub Checker

A Python tool to check if a GitHub repository exists and optionally run its test suite by leveraging HTTP status codes and cloning repositories.

## Features

- ✅ Validates GitHub repository URLs
- ✅ Checks repository existence without authentication
- ✅ **Clone and run test suites** from discovered repositories
- ✅ Returns clear status: "found", "not found", "tests passed", "tests failed", or "invalid URL"
- ✅ Uses HTTP HEAD/GET requests for checking existence
- ✅ Supports automated test execution with `uv` and pytest

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (project and dependency manager)

## Installation

Clone the repository and install dependencies using `uv`:

```bash
uv sync
```

## Usage

Run the tool with a GitHub repository URL as an argument:

```bash
uv run github-checker "<github-repo-url>"
```

To also run the repository's test suite:

```bash
uv run github-checker --run-tests "<github-repo-url>"
```

Or use the short flag:

```bash
uv run github-checker -t "<github-repo-url>"
```

### Examples

```bash
# Check if repository exists
$ uv run github-checker "https://github.com/LulaLopezKuryluk/my-project"
found

# Check and run tests
$ uv run github-checker --run-tests "https://github.com/LulaLopezKuryluk/autograde"
tests passed: 17 tests

# Invalid repository
$ uv run github-checker "https://github.com/nonexistent/repo"
not found

# Invalid URL format
$ uv run github-checker "https://invalid-domain.com/user/repo"
invalid URL
```

## Running Tests

Execute the test suite with pytest via uv:

```bash
uv run pytest
```

Or run with verbose output:

```bash
uv run pytest -v
```

## Project Structure

```
.
├── src/
│   └── github_checker/
│       ├── __init__.py
│       ├── __main__.py
│       └── checker.py
├── tests/
│   └── test_checker.py
├── pyproject.toml
└── README.md
```

## License

MIT
