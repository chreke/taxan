# Related models style guide

- Add a "style guide" section to CLAUDE.md that says whenever a model has a
  foreign key, it should" specify the `related_name` name field. The
  `related_name` should be the plural form of the model name.
- Apply the style guide to the current code base; don't forget to update
  models, serializers and to apply migrations
- Run all the tests and make sure they pass
