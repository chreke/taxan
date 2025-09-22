import pytest
from rest_framework.test import APIRequestFactory
from decimal import Decimal
from datetime import date
from tx.models import FinancialYear, Account, Event, Transaction
from tx.serializers import (
    FinancialYearSerializer,
    TransactionSerializer,
    EventSerializer,
    NestedTransactionSerializer
)


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.fixture
def api_request(api_factory):
    return api_factory.get('/')


@pytest.fixture
def valid_financial_year_data():
    return {
        'start_date': '2023-01-01',
        'end_date': '2023-12-31'
    }


@pytest.fixture
def financial_year():
    return FinancialYear.objects.create(
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31)
    )


@pytest.fixture
def account():
    return Account.objects.create(name="Cash", code=1930)


@pytest.fixture
def event(financial_year):
    return Event.objects.create(
        date=date(2023, 6, 1),
        description="Test event",
        financial_year=financial_year
    )


@pytest.fixture
def cash_account():
    return Account.objects.create(name="Cash", code=1930)


@pytest.fixture
def revenue_account():
    return Account.objects.create(name="Revenue", code=3000)


@pytest.mark.django_db
def test_financial_year_valid_dates(valid_financial_year_data):
    serializer = FinancialYearSerializer(data=valid_financial_year_data)
    assert serializer.is_valid()
    financial_year = serializer.save()
    assert financial_year.start_date == date(2023, 1, 1)
    assert financial_year.end_date == date(2023, 12, 31)


@pytest.mark.django_db
def test_financial_year_end_date_before_start_date():
    invalid_data = {
        'start_date': '2023-12-31',
        'end_date': '2023-01-01'
    }
    serializer = FinancialYearSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors


@pytest.mark.django_db
def test_financial_year_same_start_and_end_date():
    same_date_data = {
        'start_date': '2023-01-01',
        'end_date': '2023-01-01'
    }
    serializer = FinancialYearSerializer(data=same_date_data)
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors


@pytest.mark.django_db
def test_financial_year_serialization(financial_year, api_request):
    serializer = FinancialYearSerializer(financial_year, context={'request': api_request})
    data = serializer.data

    assert data['id'] == financial_year.id
    assert data['start_date'] == '2023-01-01'
    assert data['end_date'] == '2023-12-31'
    assert 'url' in data


@pytest.mark.django_db
def test_transaction_create(account, event):
    data = {
        'amount': '100.50',
        'account': account.id,
        'direction': 'debit',
        'event': event.id
    }
    serializer = TransactionSerializer(data=data)
    assert serializer.is_valid()
    transaction = serializer.save()
    assert transaction.amount == Decimal('100.50')
    assert transaction.account == account
    assert transaction.direction == 'debit'
    assert transaction.event == event


@pytest.mark.django_db
def test_transaction_invalid_direction(account, event):
    data = {
        'amount': '100.50',
        'account': account.id,
        'direction': 'invalid',
        'event': event.id
    }
    serializer = TransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'direction' in serializer.errors


@pytest.mark.django_db
def test_transaction_serialization(account, event):
    transaction = Transaction.objects.create(
        amount=Decimal('100.50'),
        account=account,
        direction='credit',
        event=event
    )
    serializer = TransactionSerializer(transaction)
    data = serializer.data

    assert data['id'] == transaction.id
    assert data['amount'] == '100.50'
    assert data['account'] == account.id
    assert data['direction'] == 'credit'
    assert data['event'] == event.id


@pytest.mark.django_db
def test_transaction_update_not_supported(account, event):
    transaction = Transaction.objects.create(
        amount=Decimal('100.50'),
        account=account,
        direction='credit',
        event=event
    )
    serializer = TransactionSerializer(transaction)
    with pytest.raises(AttributeError):
        serializer.update(transaction, {'amount': '200.00'})


@pytest.mark.django_db
def test_event_create_with_balanced_transactions(cash_account, revenue_account, financial_year):
    data = {
        'date': '2023-06-01',
        'description': 'Sale transaction',
        'financial_year': financial_year.id,
        'transactions': [
            {
                'amount': '100.00',
                'account': cash_account.id,
                'direction': 'debit'
            },
            {
                'amount': '100.00',
                'account': revenue_account.id,
                'direction': 'credit'
            }
        ]
    }
    serializer = EventSerializer(data=data)
    assert serializer.is_valid()
    event = serializer.save()

    assert event.description == 'Sale transaction'
    assert event.transactions.count() == 2

    debit_transaction = event.transactions.get(direction='debit')
    credit_transaction = event.transactions.get(direction='credit')

    assert debit_transaction.amount == Decimal('100.00')
    assert credit_transaction.amount == Decimal('100.00')


@pytest.mark.django_db
def test_event_create_with_unbalanced_transactions(cash_account, revenue_account, financial_year):
    data = {
        'date': '2023-06-01',
        'description': 'Unbalanced transaction',
        'financial_year': financial_year.id,
        'transactions': [
            {
                'amount': '100.00',
                'account': cash_account.id,
                'direction': 'debit'
            },
            {
                'amount': '50.00',
                'account': revenue_account.id,
                'direction': 'credit'
            }
        ]
    }
    serializer = EventSerializer(data=data)
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors


@pytest.mark.django_db
def test_event_create_multiple_transactions_balanced(cash_account, revenue_account, financial_year):
    expense_account = Account.objects.create(name="Expenses", code=5000)
    data = {
        'date': '2023-06-01',
        'description': 'Complex transaction',
        'financial_year': financial_year.id,
        'transactions': [
            {
                'amount': '150.00',
                'account': cash_account.id,
                'direction': 'debit'
            },
            {
                'amount': '50.00',
                'account': expense_account.id,
                'direction': 'debit'
            },
            {
                'amount': '200.00',
                'account': revenue_account.id,
                'direction': 'credit'
            }
        ]
    }
    serializer = EventSerializer(data=data)
    assert serializer.is_valid()
    event = serializer.save()
    assert event.transactions.count() == 3


@pytest.mark.django_db
def test_event_serialization(cash_account, revenue_account, financial_year, api_request):
    event = Event.objects.create(
        date=date(2023, 6, 1),
        description="Test event",
        financial_year=financial_year
    )
    Transaction.objects.create(
        amount=Decimal('100.00'),
        account=cash_account,
        direction='debit',
        event=event
    )
    Transaction.objects.create(
        amount=Decimal('100.00'),
        account=revenue_account,
        direction='credit',
        event=event
    )

    serializer = EventSerializer(event, context={'request': api_request})
    data = serializer.data

    assert data['description'] == 'Test event'
    assert len(data['transactions']) == 2
    assert data['date'] == '2023-06-01'
    assert 'url' in data

    for transaction in data['transactions']:
        assert 'amount' in transaction
        assert 'account' in transaction
        assert 'direction' in transaction
        assert 'event' not in transaction


@pytest.mark.django_db
def test_event_update_not_supported(financial_year):
    event = Event.objects.create(
        date=date(2023, 6, 1),
        description="Test event",
        financial_year=financial_year
    )
    serializer = EventSerializer(event)
    with pytest.raises(AttributeError):
        serializer.update(event, {'description': 'Updated description'})