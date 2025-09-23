# CLAUDE.md

## About

"Taxan" is an accounting service for Swedish small businesses. The service
supports bookkeeping and accounting.

## Development workflow

- Please commit your changes when you are done.
- This app uses uv for dependency management. Use `uv sync` to install dependencies.
- After making code changes, always run the tests and ensure that they pass.
- When adding dependencies, use `uv add <package>` which automatically updates pyproject.toml and uv.lock
- Please run the following command when you have completed a task:
  `afplay /System/Library/Sounds/Glass.aiff`

## Project documentation

See @docs/OVERVIEW.md for an overiew of the project. This file is written for
the benefit of you, Claude, to help you understand the project better. Please
keep this in mind if you update the file.

## Style Guide

### REST API Urls

Each serializer should have an `HyperlinkedIdentityField` field named `url`.

### Model Foreign Keys

When defining foreign keys in Django models, always specify a `related_name`
attribute. The `related_name` should be the plural form of the model name:

**Example:**

```python
class Transaction(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
```

### Code Formatting

Use `black` for Python code formatting. To format the codebase, run:

```bash
uv run black taxan tx
```
