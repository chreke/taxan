# CLAUDE.md

## About

"Taxan" is an accounting service for Swedish small businesses. The service
supports bookkeeping and accounting.

## Tech stack

- Python 3
- Django 5
- SQLite
- virtualenv

## Project structure

The main app is in the `tx` directory

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
