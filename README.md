# GitHub Checker

A simple Python tool to check if a GitHub repository exists by leveraging HTTP status codes instead of the GitHub API.

## Features

- ✅ Validates GitHub repository URLs
- ✅ Checks repository existence without authentication
- ✅ Returns clear status: "found", "not found", or "invalid URL"
- ✅ Uses HTTP HEAD/GET requests instead of API calls

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

### Examples

```bash
# Valid repository that exists
$ uv run github-checker "https://github.com/LulaLopezKuryluk/my-project"
found

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
