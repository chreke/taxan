from django.test import TestCase
from rest_framework.test import APITestCase
from decimal import Decimal
from datetime import date
from tx.models import FinancialYear, Account, Event, Transaction
from tx.serializers import (
    FinancialYearSerializer,
    TransactionSerializer,
    EventSerializer,
    NestedTransactionSerializer
)


class FinancialYearSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        }

    def test_valid_dates(self):
        serializer = FinancialYearSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        financial_year = serializer.save()
        self.assertEqual(financial_year.start_date, date(2023, 1, 1))
        self.assertEqual(financial_year.end_date, date(2023, 12, 31))

    def test_end_date_before_start_date(self):
        invalid_data = {
            'start_date': '2023-12-31',
            'end_date': '2023-01-01'
        }
        serializer = FinancialYearSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_same_start_and_end_date(self):
        same_date_data = {
            'start_date': '2023-01-01',
            'end_date': '2023-01-01'
        }
        serializer = FinancialYearSerializer(data=same_date_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_serialization(self):
        financial_year = FinancialYear.objects.create(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31)
        )
        serializer = FinancialYearSerializer(financial_year)
        expected_data = {
            'id': financial_year.id,
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        }
        self.assertEqual(serializer.data, expected_data)


class TransactionSerializerTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(name="Cash", code=1930)
        self.financial_year = FinancialYear.objects.create(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31)
        )
        self.event = Event.objects.create(
            date=date(2023, 6, 1),
            description="Test event",
            financial_year=self.financial_year
        )

    def test_create_transaction(self):
        data = {
            'amount': '100.50',
            'account': self.account.id,
            'direction': 'debit',
            'event': self.event.id
        }
        serializer = TransactionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        transaction = serializer.save()
        self.assertEqual(transaction.amount, Decimal('100.50'))
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.direction, 'debit')
        self.assertEqual(transaction.event, self.event)

    def test_invalid_direction(self):
        data = {
            'amount': '100.50',
            'account': self.account.id,
            'direction': 'invalid',
            'event': self.event.id
        }
        serializer = TransactionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('direction', serializer.errors)

    def test_serialization(self):
        transaction = Transaction.objects.create(
            amount=Decimal('100.50'),
            account=self.account,
            direction='credit',
            event=self.event
        )
        serializer = TransactionSerializer(transaction)
        expected_data = {
            'id': transaction.id,
            'amount': '100.50',
            'account': self.account.id,
            'direction': 'credit',
            'event': self.event.id
        }
        self.assertEqual(serializer.data, expected_data)

    def test_update_not_supported(self):
        transaction = Transaction.objects.create(
            amount=Decimal('100.50'),
            account=self.account,
            direction='credit',
            event=self.event
        )
        serializer = TransactionSerializer(transaction)
        # The serializer should be read-only for updates
        with self.assertRaises(AttributeError):
            serializer.update(transaction, {'amount': '200.00'})


class EventSerializerTest(TestCase):
    def setUp(self):
        self.cash_account = Account.objects.create(name="Cash", code=1930)
        self.revenue_account = Account.objects.create(name="Revenue", code=3000)
        self.financial_year = FinancialYear.objects.create(
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31)
        )

    def test_create_event_with_balanced_transactions(self):
        data = {
            'date': '2023-06-01',
            'description': 'Sale transaction',
            'financial_year': self.financial_year.id,
            'transactions': [
                {
                    'amount': '100.00',
                    'account': self.cash_account.id,
                    'direction': 'debit'
                },
                {
                    'amount': '100.00',
                    'account': self.revenue_account.id,
                    'direction': 'credit'
                }
            ]
        }
        serializer = EventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        event = serializer.save()

        self.assertEqual(event.description, 'Sale transaction')
        self.assertEqual(event.transactions.count(), 2)

        debit_transaction = event.transactions.get(direction='debit')
        credit_transaction = event.transactions.get(direction='credit')

        self.assertEqual(debit_transaction.amount, Decimal('100.00'))
        self.assertEqual(credit_transaction.amount, Decimal('100.00'))

    def test_create_event_with_unbalanced_transactions(self):
        data = {
            'date': '2023-06-01',
            'description': 'Unbalanced transaction',
            'financial_year': self.financial_year.id,
            'transactions': [
                {
                    'amount': '100.00',
                    'account': self.cash_account.id,
                    'direction': 'debit'
                },
                {
                    'amount': '50.00',
                    'account': self.revenue_account.id,
                    'direction': 'credit'
                }
            ]
        }
        serializer = EventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_create_event_multiple_transactions_balanced(self):
        expense_account = Account.objects.create(name="Expenses", code=5000)
        data = {
            'date': '2023-06-01',
            'description': 'Complex transaction',
            'financial_year': self.financial_year.id,
            'transactions': [
                {
                    'amount': '150.00',
                    'account': self.cash_account.id,
                    'direction': 'debit'
                },
                {
                    'amount': '50.00',
                    'account': expense_account.id,
                    'direction': 'debit'
                },
                {
                    'amount': '200.00',
                    'account': self.revenue_account.id,
                    'direction': 'credit'
                }
            ]
        }
        serializer = EventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        event = serializer.save()
        self.assertEqual(event.transactions.count(), 3)

    def test_serialization(self):
        event = Event.objects.create(
            date=date(2023, 6, 1),
            description="Test event",
            financial_year=self.financial_year
        )
        Transaction.objects.create(
            amount=Decimal('100.00'),
            account=self.cash_account,
            direction='debit',
            event=event
        )
        Transaction.objects.create(
            amount=Decimal('100.00'),
            account=self.revenue_account,
            direction='credit',
            event=event
        )

        serializer = EventSerializer(event)
        data = serializer.data

        self.assertEqual(data['description'], 'Test event')
        self.assertEqual(len(data['transactions']), 2)
        self.assertEqual(data['date'], '2023-06-01')

        # Check that transactions don't include 'event' field in nested format
        for transaction in data['transactions']:
            self.assertIn('amount', transaction)
            self.assertIn('account', transaction)
            self.assertIn('direction', transaction)
            self.assertNotIn('event', transaction)

    def test_update_not_supported(self):
        event = Event.objects.create(
            date=date(2023, 6, 1),
            description="Test event",
            financial_year=self.financial_year
        )
        serializer = EventSerializer(event)
        # The serializer should be read-only for updates
        with self.assertRaises(AttributeError):
            serializer.update(event, {'description': 'Updated description'})