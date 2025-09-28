import uuid
import os
from django.db import models


class FinancialYear(models.Model):
    start_date = models.DateField(help_text="The first day of the financial year")
    end_date = models.DateField(help_text="The last day of the financial year")

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


class Account(models.Model):
    name = models.CharField(
        max_length=255, blank=False, help_text="Descriptive name of the account"
    )
    code = models.IntegerField(help_text="Numerical identifier for the account")

    def __str__(self):
        return f"{self.code} - {self.name}"


class Event(models.Model):
    date = models.DateField(help_text="The date when this accounting event occurred")
    description = models.CharField(
        max_length=100, help_text="Brief description of the accounting event"
    )
    financial_year = models.ForeignKey(
        FinancialYear,
        on_delete=models.CASCADE,
        related_name="events",
        help_text="Optional financial year this event belongs to",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this event was created in the system",
    )

    def __str__(self):
        return f"{self.date} - {self.description}"


class Transaction(models.Model):
    DIRECTION_CHOICES = [
        ("debit", "Debit"),
        ("credit", "Credit"),
    ]

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Transaction amount with up to 12 digits and 2 decimal places",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text="The account this transaction affects",
    )
    direction = models.CharField(
        max_length=6,
        choices=DIRECTION_CHOICES,
        help_text="Whether this is a debit or credit transaction",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text="The event this transaction belongs to",
    )

    def __str__(self):
        return f"{self.direction} {self.amount} to {self.account.name}"


def attachment_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("attachments", filename)


class Attachment(models.Model):
    file = models.FileField(
        upload_to=attachment_upload_to,
        help_text="Uploaded file attachment (renamed with UUID)",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="attachments",
        help_text="The event this attachment is associated with",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when this attachment was uploaded"
    )

    def __str__(self):
        return f"Attachment for {self.event.description}"
