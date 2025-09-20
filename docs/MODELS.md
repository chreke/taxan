# Models Documentation

This document describes the Django models used in the Taxan accounting system.

## Account

The `Account` model represents an account in the accounting ledger.

### Fields

- `name` The common name of the account (e.g., "Cash", "Accounts Receivable")
- `code` The numerical account code used in the chart of accounts (e.g., 1930)


## Event

The `Event` model represents a bookkeeping event that groups related transactions.

### Fields

- `date` The date when the event occurred
- `description` A free text description of the event

## Transaction

The `Transaction` model represents individual debit or credit transactions within an accounting event.

### Fields

- `amount` The monetary amount of the transaction
- `account` Reference to the account being debited or credited
- `direction` Either "debit" or "credit"
- `event` Reference to the bookkeeping event this transaction belongs to

## Model Relationships

- Each `Transaction` belongs to one `Account` and one `Event`
- Each `Event` can have multiple `Transaction` entries
- Each `Account` can be referenced by multiple `Transaction` entries

## Double-Entry Bookkeeping

The system follows double-entry bookkeeping principles where every `Event` should have balanced debits and credits (total debits = total credits).
