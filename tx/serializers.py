from rest_framework import serializers
from decimal import Decimal
from .models import FinancialYear, Account, Event, Transaction


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = ['id', 'start_date', 'end_date']

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError(
                "Start date must be before end date."
            )
        return data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'account', 'direction', 'event']
        read_only_fields = []

    def update(self, instance, validated_data):
        raise AttributeError("Transaction updates are not supported")


class NestedTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'account', 'direction']


class EventSerializer(serializers.ModelSerializer):
    transactions = NestedTransactionSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'date', 'description', 'financial_year', 'transactions', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        transactions_data = data.get('transactions', [])

        if not transactions_data:
            raise serializers.ValidationError(
                "Event must have at least one transaction."
            )

        total_debits = Decimal('0')
        total_credits = Decimal('0')

        for transaction_data in transactions_data:
            amount = transaction_data['amount']
            direction = transaction_data['direction']

            if direction == 'debit':
                total_debits += amount
            elif direction == 'credit':
                total_credits += amount

        if total_debits != total_credits:
            raise serializers.ValidationError(
                f"Total debits ({total_debits}) must equal total credits ({total_credits})."
            )

        return data

    def create(self, validated_data):
        transactions_data = validated_data.pop('transactions')
        event = Event.objects.create(**validated_data)

        for transaction_data in transactions_data:
            Transaction.objects.create(event=event, **transaction_data)

        return event

    def update(self, instance, validated_data):
        raise AttributeError("Event updates are not supported")