# Upload attachments

It should be possible to upload attachments.

There should be an Attachment model with the following fields:
(required unless otherwise noted)

- file: A file upload field
- event: A foreign key to an event
- created_at: Datetime (defaults to "now")

The file should be renamed to a generated UUID (but with the file extension
intact) e.g. if I upload "receipt.jpg" it should be renamed to
$SOME_UUID.jpg, given that $SOME_UUID is an auto-generated UUID

Please consult `docs/MODELS.md` to understand the model structure

Also, make sure to set up MEDIA_ROOT and MEDIA_URL settings.

Make sure the attachmetns get uploaded to an "attachments" subdirectory

The serializers should also be updated:

- Add a *read-only* field to the Event serializer for its attachments
- Add a new serializer for uploading files; add it to the DRF browser

Update tests as appropriate and make sure they pass. Add some basic tests
for uploading attachments.

When you are done, please update `docs/MODELS.md` and document the
new model. Also, update `docs/OVERVIEW.md` with the high-level
change we've made to the project.
