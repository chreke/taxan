import uuid
import os
from django.db import models


class FinancialYear(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


class Account(models.Model):
    name = models.CharField(max_length=255, blank=False)
    code = models.IntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"


class Event(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=100)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, null=True, blank=True, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.description}"


class Transaction(models.Model):
    DIRECTION_CHOICES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    direction = models.CharField(max_length=6, choices=DIRECTION_CHOICES)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f"{self.direction} {self.amount} to {self.account.name}"


def attachment_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join('attachments', filename)


class Attachment(models.Model):
    file = models.FileField(upload_to=attachment_upload_to)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attachments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.event.description}"
