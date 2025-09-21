# Models Documentation

This document describes the Django models used in the Taxan accounting system.

## FinancialYear

The `FinancialYear` model represents a business's financial year period, which can be different from a fiscal year.

### Fields

- `start_date` The start date of the financial year
- `end_date` The end date of the financial year

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
- `financial_year` Reference to the financial year this event belongs to (optional)

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
- Each `Event` can optionally belong to one `FinancialYear`
- Each `FinancialYear` can have multiple `Event` entries
- Each `Account` can be referenced by multiple `Transaction` entries
