# Taxan

"Taxan" is an accounting service for Swedish small businesses. The service supports bookkeeping and accounting.

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for fast dependency management.

```bash
# Install dependencies
uv sync

# Run migrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Start development server
uv run python manage.py runserver
```
