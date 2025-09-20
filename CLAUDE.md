# CLAUDE.md

Please run the following command when you have completed a task:
`afplay /System/Library/Sounds/Glass.aiff`

## About

"Taxan" is an accounting service for Swedish small businesses. The service
supports bookkeeping and accounting.

## Tech stack

- Python 3
- Django 5
- Django REST Framework
- SQLite
- virtualenv

## Project structure

```
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── docs/MODELS.md              # Database models documentation
├── taxan/                      # Django project configuration
└── tx/                         # Main accounting app
    ├── models.py               # Database models
    ├── serializers.py          # API serializers
    ├── views.py                # View functions
    ├── admin.py                # Django admin configuration
    └── tests.py                # Test cases
```

## Development workflow

Please commit your changes when you are done.

## Development Setup

Note that this app uses a virtual environment located in `venv`; please make
sure it is sourced it before attempting to run any Python or Django commands.

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Common Commands

```bash
# Create new app
python manage.py startapp <app_name>

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test
```

## Style Guide

### Model Foreign Keys

When defining foreign keys in Django models, always specify a `related_name` attribute. The `related_name` should be the plural form of the model name to maintain consistency and clarity in reverse lookups.

**Example:**
```python
class Transaction(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
```

This allows for intuitive reverse queries like `event.transactions.all()` and `account.transactions.all()`.
