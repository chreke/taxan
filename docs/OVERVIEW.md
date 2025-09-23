# Taxan - Accounting Service Code Overview

## Project Architecture

**Taxan** is a Django-based accounting service designed for Swedish small businesses, providing bookkeeping and accounting functionality using double-entry bookkeeping principles.

### Technology Stack
- **Backend**: Python 3 with Django 5.2.6
- **API Framework**: Django REST Framework 3.16.1
- **API Documentation**: drf-spectacular for OpenAPI 3.0 schema generation
- **Database**: SQLite (development)
- **Testing**: pytest with pytest-django
- **Package Management**: uv for fast dependency resolution and installation

## Core Components

### 1. Models (`tx/models.py`)

The application implements four main models following double-entry bookkeeping principles:

**FinancialYear**
- Represents business fiscal periods
- Fields: `start_date`, `end_date`
- Validation ensures start_date < end_date

**Account**
- Chart of accounts implementation
- Fields: `name` (account description), `code` (numerical identifier)
- Example: "Cash" with code 1930

**Event**
- Groups related transactions (journal entries)
- Fields: `date`, `description`, `financial_year` (optional FK), `created_at` (auto-timestamp)
- One Event can contain multiple balanced Transactions

**Transaction**
- Individual debit/credit entries
- Fields: `amount` (decimal), `account` (FK), `direction` (debit/credit), `event` (FK)
- Enforces double-entry principle through validation

**Attachment**
- File attachments for events (receipts, invoices, etc.)
- Fields: `file` (FileField with UUID naming), `event` (FK), `created_at` (auto-timestamp)
- Files uploaded to 'attachments' subdirectory with UUID-based filenames

### 2. API Layer (`tx/views.py`, `tx/serializers.py`)

**ViewSets**:
- `EventViewSet`: Full CRUD for accounting events
- `FinancialYearViewSet`: Financial year management
- `AttachmentViewSet`: File upload and management for event attachments
- All use `ModelViewSet` for standard REST operations

**Serializers** implement strict business logic:
- `EventSerializer`: Creates events with nested transactions, validates balanced entries, includes read-only attachments
- `FinancialYearSerializer`: Validates date ranges
- `TransactionSerializer`: Individual transaction handling
- `NestedTransactionSerializer`: Used within event creation
- `AttachmentSerializer`: File upload handling with event association

**Key Business Rules**:
- Events must have at least one transaction
- Total debits must equal total credits (double-entry validation)
- Events and Transactions are immutable after creation (updates disabled)
- Automatic decimal precision handling for monetary values

### 3. URL Configuration (`taxan/urls.py`)

RESTful API endpoints:
- `/events/` - Event CRUD operations
- `/financial-years/` - Financial year management
- `/attachments/` - File upload and attachment management
- `/api/schema/` - OpenAPI 3.0 schema (JSON format)
- `/api/docs/` - Interactive Swagger UI documentation
- `/admin/` - Django admin interface
- `/api-auth/` - DRF authentication
- `/media/` - Uploaded file serving (development only)

### 4. Testing (`tx/tests/`)

Comprehensive test coverage with dedicated test modules:

**`test_serializers.py`**: Serializer validation logic, data transformation, and business rules
**`test_views.py`**: API endpoint functionality and HTTP responses
**`test_attachments.py`**: File upload functionality, UUID generation, and event integration

Tests verify:
- Double-entry bookkeeping validation
- Date validation for financial years
- Immutability of financial records
- File upload functionality with UUID-based naming
- Proper error handling and business rule enforcement

**Test Execution**: Run tests using `pytest` command (configured via pyproject.toml)

### 5. Configuration (`taxan/settings.py`)

Standard Django configuration with:
- SQLite database for development
- Django REST Framework integration with drf-spectacular for OpenAPI schema generation
- Single app (`tx`) registration
- Development-friendly settings (DEBUG=True)
- Media file handling (MEDIA_ROOT, MEDIA_URL) for attachments

## Data Flow

1. **Event Creation**: Client submits event with nested transactions
2. **Validation**: EventSerializer validates balanced debits/credits
3. **Persistence**: Event and related transactions saved atomically
4. **Immutability**: No updates allowed to maintain audit trail

## Key Design Decisions

- **Immutable Records**: Events and transactions cannot be updated, ensuring audit integrity
- **Nested Transaction Creation**: Transactions created within event context for data consistency
- **Strict Validation**: Double-entry bookkeeping rules enforced at serializer level
- **Decimal Precision**: Proper monetary value handling with decimal fields
- **Related Names**: Consistent use of plural forms for reverse relationships

The codebase demonstrates solid Django/DRF practices with proper separation of concerns, comprehensive testing, and adherence to accounting principles.