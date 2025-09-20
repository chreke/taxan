from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tx.models import Event, FinancialYear, Account


class EventViewSetTestCase(APITestCase):
    def setUp(self):
        self.financial_year = FinancialYear.objects.create(
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        self.account = Account.objects.create(
            name='Test Account',
            code=1000
        )

    def test_create_event(self):
        url = reverse('event-list')
        data = {
            'date': '2023-06-15',
            'description': 'Test Event',
            'financial_year': self.financial_year.id,
            'transactions': [
                {
                    'amount': '100.00',
                    'account': self.account.id,
                    'direction': 'debit'
                },
                {
                    'amount': '100.00',
                    'account': self.account.id,
                    'direction': 'credit'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.description, 'Test Event')
        self.assertEqual(event.transactions.count(), 2)

    def test_get_event(self):
        event = Event.objects.create(
            date='2023-06-15',
            description='Test Event',
            financial_year=self.financial_year
        )
        url = reverse('event-detail', kwargs={'pk': event.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test Event')

    def test_list_events(self):
        Event.objects.create(
            date='2023-06-15',
            description='Test Event 1',
            financial_year=self.financial_year
        )
        Event.objects.create(
            date='2023-06-16',
            description='Test Event 2',
            financial_year=self.financial_year
        )
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)