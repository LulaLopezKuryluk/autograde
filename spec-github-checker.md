# Spec 001: GitHub Repository existence checker 

## Behavior
- The app should only accept a valid GitHub repository URL as input.
- The app should return "not found" if the repository does not exist.
- The app should return "found" if the repository exists.
- The app should return "invalid URL" if the input is not a valid GitHub repository URL.

## Constraints
- The app should be as simple as possible while meeting the behavior requirements.
- The app should not use the GitHub API and leverage HTTP status codes instead.
- The app should be implemented in Python.
- The app should be designed for maintainability and extensibility.
- The app should use uv as project and dependency manager.
- The app should use pytest for testing, if tests are needed.

## Out of scope
- The app does not need to support private repositories or authentication.