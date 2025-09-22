import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from tx.models import Event, FinancialYear, Account


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def financial_year():
    return FinancialYear.objects.create(
        start_date='2023-01-01',
        end_date='2023-12-31'
    )


@pytest.fixture
def account():
    return Account.objects.create(
        name='Test Account',
        code=1000
    )


@pytest.mark.django_db
def test_create_event(api_client, financial_year, account):
    url = reverse('event-list')
    data = {
        'date': '2023-06-15',
        'description': 'Test Event',
        'financial_year': financial_year.id,
        'transactions': [
            {
                'amount': '100.00',
                'account': account.id,
                'direction': 'debit'
            },
            {
                'amount': '100.00',
                'account': account.id,
                'direction': 'credit'
            }
        ]
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Event.objects.count() == 1
    event = Event.objects.first()
    assert event.description == 'Test Event'
    assert event.transactions.count() == 2


@pytest.mark.django_db
def test_get_event(api_client, financial_year):
    event = Event.objects.create(
        date='2023-06-15',
        description='Test Event',
        financial_year=financial_year
    )
    url = reverse('event-detail', kwargs={'pk': event.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['description'] == 'Test Event'


@pytest.mark.django_db
def test_list_events(api_client, financial_year):
    Event.objects.create(
        date='2023-06-15',
        description='Test Event 1',
        financial_year=financial_year
    )
    Event.objects.create(
        date='2023-06-16',
        description='Test Event 2',
        financial_year=financial_year
    )
    url = reverse('event-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2