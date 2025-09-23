# Taxan - Accounting Service Code Overview

## Project Architecture

**Taxan** is a Django-based accounting service implementing double-entry bookkeeping principles.

### Technology Stack
- **Backend**: Django with Django REST Framework
- **API Documentation**: drf-spectacular for OpenAPI schema generation
- **Testing**: pytest with pytest-django
- **Package Management**: uv

## Core Components

### 1. Models (`tx/models.py`)

The application implements four main models following double-entry bookkeeping principles:

**FinancialYear**
- Represents business fiscal periods
- Fields: `start_date`, `end_date`
- Validation ensures start_date < end_date

**Account**
- Chart of accounts implementation
- Fields: `name`, `code` (numerical identifier)

**Event**
- Groups related transactions (journal entries)
- Fields: `date`, `description`, `financial_year` (optional FK), `created_at`
- Contains multiple balanced Transactions

**Transaction**
- Individual debit/credit entries
- Fields: `amount`, `account` (FK), `direction` (debit/credit), `event` (FK)
- Enforces double-entry principle

**Attachment**
- File attachments for events
- Fields: `file` (FileField with UUID naming), `event` (FK), `created_at`

### 2. API Layer (`tx/views.py`, `tx/serializers.py`)

**ViewSets**: `EventViewSet`, `FinancialYearViewSet`, `AttachmentViewSet` - all use `ModelViewSet`

**Serializers**:
- `EventSerializer`: Creates events with nested transactions, validates balanced entries
- `FinancialYearSerializer`: Validates date ranges
- `TransactionSerializer`: Individual transaction handling
- `NestedTransactionSerializer`: Used within event creation
- `AttachmentSerializer`: File upload handling

**Key Business Rules**:
- Events must have at least one transaction
- Total debits must equal total credits
- Events and Transactions are immutable after creation

### 3. URL Configuration (`taxan/urls.py`)

RESTful API endpoints:
- `/events/` - Event CRUD operations
- `/financial-years/` - Financial year management
- `/attachments/` - File upload and attachment management
- `/schema/` - OpenAPI 3.0 schema (JSON format)
- `/docs/` - Interactive Swagger UI documentation
- `/admin/` - Django admin interface
- `/api-auth/` - DRF authentication
- `/media/` - Uploaded file serving (development only)

### 4. Testing (`tx/tests/`)

Test modules:
- `test_serializers.py`: Serializer validation and business rules
- `test_views.py`: API endpoint functionality
- `test_attachments.py`: File upload functionality

**Test Execution**: Run tests using `pytest`

### 5. Configuration (`taxan/settings.py`)

Standard Django configuration with:
- Django REST Framework integration with drf-spectacular
- Single app (`tx`) registration
- Media file handling for attachments

## Key Design Decisions

- **Immutable Records**: Events and transactions cannot be updated
- **Nested Transaction Creation**: Transactions created within event context
- **Double-entry Validation**: Enforced at serializer level
- **Related Names**: Consistent use of plural forms for reverse relationships