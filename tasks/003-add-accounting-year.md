# Add "financial year" model

I forgot to add a "financial year" model; 

The "financial year" model represents the business' financial year; this can be different from a fiscal year (e.g. some businesses have financial years that span from summer to summer, for example)

The financial year model should have the following fields:

- Start date
- End date

Each Event should have a ForeignKey referencing a financial year. The db is empty so it's fine to go ahead and add the foreign key.

Reference docs/MODELS.md for a description of the db. Please update docs/MODELS.md when you are done.
