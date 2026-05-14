# Agents Configuration

## Project Standards

### Dependency Management
- **Package Manager**: `uv`
- All dependencies should be managed using `uv`
- Use `uv pip install` for package installation
- Use `uv sync` to synchronize project dependencies

### Testing Framework
- **Test Runner**: `pytest`
- **Test Location**: Tests must be contained in a `tests/` folder in the root directory
- Tests should follow the naming convention: `test_*.py` or `*_test.py`
- Run tests using: `pytest tests/`

### Directory Structure
```
.
├── tests/
│   ├── test_*.py
│   └── *_test.py
├── spec-autograde.md
├── AGENTS.md
└── pyproject.toml (or uv.lock)
```

### Development Workflow
1. Use `uv` for managing Python versions and dependencies
2. Write tests in the `tests/` directory
3. Run `pytest` to execute all tests before committing changes
