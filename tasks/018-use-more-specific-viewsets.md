# Use more specific viewsets

Viewsets should be more specific. Unless a viewset supports all CRUD operations,
it should use a combination of GenericViewSet and appropriate mixins (i.e.
CreateModelMixin, ListModelMixin, RetrieveModelMixin, DeleteModelMixin,
UpdateModelMixin)

- EventViewSet should only support list, retrieve and create 
- FinancialYearViewSet should only support list, retrieve and create
- AttachmentViewSet can remain a ModelViewSet

Please update the OpenAPI documentation to reflect this
