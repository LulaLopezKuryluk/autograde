# AutoGrade

Simple CLI tool for repository validation.

## Install

Use `uv` to install project dependencies:

```bash
uv install
```

If you prefer a direct Python install, run:

```bash
python -m pip install -e .
```

## Run the tool

After installing, run the CLI with:

```bash
autograde <args>
```

If you want to run it through `uv` without installing globally:

```bash
uv exec autograde -- <args>
```

## Run tests

Use `pytest` to execute the test suite:

```bash
pytest tests/
```

With `uv`:

```bash
uv exec pytest tests/
```
