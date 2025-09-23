from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from .models import FinancialYear, Account, Event, Transaction, Attachment


class FinancialYearSerializer(serializers.ModelSerializer):
    """
    Serializer for financial year entities representing business fiscal periods.
    Financial years define the accounting periods for organizing business transactions.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="financialyear-detail",
        help_text="URL to access this financial year resource",
    )

    class Meta:
        model = FinancialYear
        fields = ["url", "id", "start_date", "end_date"]

    def validate(self, data):
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError("Start date must be before end date.")
        return data


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for individual transaction entries in double-entry bookkeeping.
    Each transaction represents either a debit or credit to a specific account.
    """

    class Meta:
        model = Transaction
        fields = ["id", "amount", "account", "direction", "event"]
        read_only_fields = []

    def update(self, instance, validated_data):
        raise AttributeError("Transaction updates are not supported")


class NestedTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for creating transactions within an event context.
    Used when creating events with nested transaction data.
    """

    class Meta:
        model = Transaction
        fields = ["amount", "account", "direction"]


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for accounting events (journal entries) with nested transactions.
    Events group related transactions and must maintain balanced debits and credits.
    Events are immutable after creation to maintain accounting integrity.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="event-detail", help_text="URL to access this event resource"
    )
    transactions = NestedTransactionSerializer(
        many=True, help_text="List of debit and credit transactions for this event"
    )
    attachments = serializers.StringRelatedField(
        many=True,
        read_only=True,
        help_text="File attachments associated with this event",
    )

    class Meta:
        model = Event
        fields = [
            "url",
            "id",
            "date",
            "description",
            "financial_year",
            "transactions",
            "attachments",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate(self, data):
        transactions_data = data.get("transactions", [])

        if not transactions_data:
            raise serializers.ValidationError(
                "Event must have at least one transaction."
            )

        total_debits = Decimal("0")
        total_credits = Decimal("0")

        for transaction_data in transactions_data:
            amount = transaction_data["amount"]
            direction = transaction_data["direction"]

            if direction == "debit":
                total_debits += amount
            elif direction == "credit":
                total_credits += amount

        if total_debits != total_credits:
            raise serializers.ValidationError(
                f"Total debits ({total_debits}) must equal total credits ({total_credits})."
            )

        return data

    def create(self, validated_data):
        transactions_data = validated_data.pop("transactions")

        with transaction.atomic():
            event = Event.objects.create(**validated_data)

            for transaction_data in transactions_data:
                Transaction.objects.create(event=event, **transaction_data)

        return event

    def update(self, instance, validated_data):
        raise AttributeError("Event updates are not supported")


class AttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer for file attachments associated with accounting events.
    Files are automatically renamed with UUIDs and stored in the attachments directory.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="attachment-detail",
        help_text="URL to access this attachment resource",
    )

    class Meta:
        model = Attachment
        fields = ["url", "id", "file", "event", "created_at"]
        read_only_fields = ["created_at"]
