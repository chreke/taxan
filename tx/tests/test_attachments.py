import os
import tempfile
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from tx.models import Event, FinancialYear, Account, Attachment


@pytest.fixture
def financial_year():
    return FinancialYear.objects.create(start_date="2023-01-01", end_date="2023-12-31")


@pytest.fixture
def account():
    return Account.objects.create(name="Test Account", code=1000)


@pytest.fixture
def event(financial_year):
    return Event.objects.create(
        date="2023-06-15", description="Test Event", financial_year=financial_year
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_attachment_creation(event):
    file_content = b"test file content"
    uploaded_file = SimpleUploadedFile(
        "test.txt", file_content, content_type="text/plain"
    )

    attachment = Attachment.objects.create(file=uploaded_file, event=event)

    assert attachment.id is not None
    assert attachment.event == event
    assert attachment.created_at is not None
    assert attachment.file.name.startswith("attachments/")
    assert attachment.file.name.endswith(".txt")


@pytest.mark.django_db
def test_attachment_upload_path_with_uuid(event):
    file_content = b"test file content"
    uploaded_file = SimpleUploadedFile(
        "receipt.jpg", file_content, content_type="image/jpeg"
    )

    attachment = Attachment.objects.create(file=uploaded_file, event=event)

    file_path = attachment.file.name
    assert file_path.startswith("attachments/")
    assert file_path.endswith(".jpg")

    filename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(filename)[0]
    assert len(name_without_ext) == 36


@pytest.mark.django_db
def test_attachment_str_representation(event):
    file_content = b"test file content"
    uploaded_file = SimpleUploadedFile(
        "test.txt", file_content, content_type="text/plain"
    )

    attachment = Attachment.objects.create(file=uploaded_file, event=event)

    expected_str = f"Attachment for {event.description}"
    assert str(attachment) == expected_str


@pytest.mark.django_db
def test_upload_attachment(api_client, event, settings):
    settings.MEDIA_ROOT = tempfile.mkdtemp()

    url = reverse("attachment-list")
    file_content = b"test file content"
    uploaded_file = SimpleUploadedFile(
        "receipt.jpg", file_content, content_type="image/jpeg"
    )

    data = {"file": uploaded_file, "event": event.id}

    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_201_CREATED
    assert Attachment.objects.count() == 1

    attachment = Attachment.objects.first()
    assert attachment.event == event
    assert attachment.file.name.endswith(".jpg")


@pytest.mark.django_db
def test_list_attachments(api_client, event):
    file_content = b"test file content"
    uploaded_file = SimpleUploadedFile(
        "test.txt", file_content, content_type="text/plain"
    )

    Attachment.objects.create(file=uploaded_file, event=event)

    url = reverse("attachment-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["event"] == event.id


@pytest.mark.django_db
def test_get_attachment_detail(api_client, event):
    file_content = b"test file content"
    uploaded_file = SimpleUploadedFile(
        "test.txt", file_content, content_type="text/plain"
    )

    attachment = Attachment.objects.create(file=uploaded_file, event=event)

    url = reverse("attachment-detail", kwargs={"pk": attachment.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == attachment.id
    assert response.data["event"] == event.id


@pytest.mark.django_db
def test_event_includes_attachments(api_client, event):
    file_content = b"test file content"
    uploaded_file = SimpleUploadedFile(
        "receipt.pdf", file_content, content_type="application/pdf"
    )

    attachment = Attachment.objects.create(file=uploaded_file, event=event)

    url = reverse("event-detail", kwargs={"pk": event.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "attachments" in response.data
    assert len(response.data["attachments"]) == 1
