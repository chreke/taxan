from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=255, blank=False)
    code = models.IntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"


class Event(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.description}"


class Transaction(models.Model):
    DIRECTION_CHOICES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    direction = models.CharField(max_length=6, choices=DIRECTION_CHOICES)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.direction.title()} {self.amount} to {self.account.name}"
