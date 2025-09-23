# Document the REST API endpoints

The REST API endpoints and their input / output schemas need to be properly
documented in the OpenAPI spec.  Currently, most of the endpoints lack OpenAPI
descriptions; there should be descriptions with enough detail that someone
could integrate with the API without needing any further documentation. Since
the other implementation will mostly be written by another Claude instance, it
should be at the level of detail where Claude can understand what each endpoint
does.
