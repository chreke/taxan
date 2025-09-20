# DRF Serializers

Let's create some serializers; create the following serializers:

- A serializer for the finanical year model; it should validate that the start
  date is before the end date.
- A serializer for the transaction model. the serializer should *only* support
  "read" and "create", not "update" or "delete"
- A serializer for an Event; it should accept a list of transactions, that get
  created on save. it should also validate that the total amount of the "debit"
  transactions are equal to the amount of "credit" transactions. the serializer
  should *only* support "read" and "create", not "update" or "delete".

Please write unit tests for these serialziers first. Save the tests to a new "tests"
directory in a module called `test_serializers.py` (don't forget to add an
`__init__.py`!)
