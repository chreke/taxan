import os
import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from tx.models import Event, FinancialYear, Account, Attachment


class AttachmentModelTestCase(TestCase):
    def setUp(self):
        self.financial_year = FinancialYear.objects.create(
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        self.event = Event.objects.create(
            date='2023-06-15',
            description='Test Event',
            financial_year=self.financial_year
        )

    def test_attachment_creation(self):
        file_content = b'test file content'
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            file_content,
            content_type='text/plain'
        )

        attachment = Attachment.objects.create(
            file=uploaded_file,
            event=self.event
        )

        self.assertIsNotNone(attachment.id)
        self.assertEqual(attachment.event, self.event)
        self.assertIsNotNone(attachment.created_at)
        self.assertTrue(attachment.file.name.startswith('attachments/'))
        self.assertTrue(attachment.file.name.endswith('.txt'))

    def test_attachment_upload_path_with_uuid(self):
        file_content = b'test file content'
        uploaded_file = SimpleUploadedFile(
            'receipt.jpg',
            file_content,
            content_type='image/jpeg'
        )

        attachment = Attachment.objects.create(
            file=uploaded_file,
            event=self.event
        )

        file_path = attachment.file.name
        self.assertTrue(file_path.startswith('attachments/'))
        self.assertTrue(file_path.endswith('.jpg'))

        # Ensure filename is a UUID (36 chars) + extension
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        self.assertEqual(len(name_without_ext), 36)  # UUID length

    def test_attachment_str_representation(self):
        file_content = b'test file content'
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            file_content,
            content_type='text/plain'
        )

        attachment = Attachment.objects.create(
            file=uploaded_file,
            event=self.event
        )

        expected_str = f"Attachment for {self.event.description}"
        self.assertEqual(str(attachment), expected_str)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class AttachmentViewSetTestCase(APITestCase):
    def setUp(self):
        self.financial_year = FinancialYear.objects.create(
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        self.account = Account.objects.create(
            name='Test Account',
            code=1000
        )
        self.event = Event.objects.create(
            date='2023-06-15',
            description='Test Event',
            financial_year=self.financial_year
        )

    def test_upload_attachment(self):
        url = reverse('attachment-list')
        file_content = b'test file content'
        uploaded_file = SimpleUploadedFile(
            'receipt.jpg',
            file_content,
            content_type='image/jpeg'
        )

        data = {
            'file': uploaded_file,
            'event': self.event.id
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attachment.objects.count(), 1)

        attachment = Attachment.objects.first()
        self.assertEqual(attachment.event, self.event)
        self.assertTrue(attachment.file.name.endswith('.jpg'))

    def test_list_attachments(self):
        # Create an attachment
        file_content = b'test file content'
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            file_content,
            content_type='text/plain'
        )

        Attachment.objects.create(
            file=uploaded_file,
            event=self.event
        )

        url = reverse('attachment-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event'], self.event.id)

    def test_get_attachment_detail(self):
        file_content = b'test file content'
        uploaded_file = SimpleUploadedFile(
            'test.txt',
            file_content,
            content_type='text/plain'
        )

        attachment = Attachment.objects.create(
            file=uploaded_file,
            event=self.event
        )

        url = reverse('attachment-detail', kwargs={'pk': attachment.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], attachment.id)
        self.assertEqual(response.data['event'], self.event.id)

    def test_event_includes_attachments(self):
        # Create an attachment for the event
        file_content = b'test file content'
        uploaded_file = SimpleUploadedFile(
            'receipt.pdf',
            file_content,
            content_type='application/pdf'
        )

        attachment = Attachment.objects.create(
            file=uploaded_file,
            event=self.event
        )

        # Get the event and check attachments are included
        url = reverse('event-detail', kwargs={'pk': self.event.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('attachments', response.data)
        self.assertEqual(len(response.data['attachments']), 1)