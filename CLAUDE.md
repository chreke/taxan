# CLAUDE.md

## About

"Taxan" is an accounting service for Swedish small businesses. The service
supports bookkeeping and accounting.

## Development workflow

- Please commit your changes when you are done.
- Note that this app uses a virtual environment located in `venv`; please make
  sure it is sourced it before attempting to run any Python or Django commands.
- After making code changes, always run the tests and ensure that they pass.
- Please run the following command when you have completed a task:
  `afplay /System/Library/Sounds/Glass.aiff`

## Project documentation

See @docs/OVERVIEW.md for an overiew of the project

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
