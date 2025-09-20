# Initial model setup

Please set up the following Django models. (All fields are mandatory
unless indicated otherwise)

## Account

The "Account" model represents an account in the accounting ledger. It
should have the following fields:

- Name (string, not blank) - the common name of the account (e.g. 
- Code (int) - the account code (e.g. 1930)

## Event

The "Event" model represents a bookkeeping event. It should have the
following fields:

- Date
- Description (free text, maximum 100 characters)

## Transaction

The "Transaction" model represents a transaction in the accounting ledger.
It should have the following fields:

- Amount (an amount of money; please use an appropriate decimal type)
- Account (foreign key to Account)
- Direction - can be either "debit" or "credit"
- Event (foreign key to Event)
