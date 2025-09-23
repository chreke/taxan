from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Event, FinancialYear, Attachment
from .serializers import EventSerializer, FinancialYearSerializer, AttachmentSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List accounting events",
        description="Retrieve a list of all accounting events (journal entries) with their transactions and attachments.",
        tags=["events"]
    ),
    create=extend_schema(
        summary="Create a new accounting event",
        description="Create a new accounting event with nested transactions. The total debits must equal total credits, and at least one transaction is required.",
        tags=["events"]
    ),
    retrieve=extend_schema(
        summary="Retrieve an accounting event",
        description="Get details of a specific accounting event including all its transactions and attachments.",
        tags=["events"]
    ),
    update=extend_schema(
        summary="Update an accounting event",
        description="Events are immutable after creation. This operation is not supported to maintain accounting integrity.",
        tags=["events"]
    ),
    partial_update=extend_schema(
        summary="Partially update an accounting event",
        description="Events are immutable after creation. This operation is not supported to maintain accounting integrity.",
        tags=["events"]
    ),
    destroy=extend_schema(
        summary="Delete an accounting event",
        description="Delete an accounting event and all its associated transactions. Use with caution as this affects accounting records.",
        tags=["events"]
    )
)
class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing accounting events (journal entries).

    Events are the core of double-entry bookkeeping, containing one or more
    transactions that must balance (total debits = total credits).
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List financial years",
        description="Retrieve a list of all defined financial years for the business.",
        tags=["financial-years"]
    ),
    create=extend_schema(
        summary="Create a new financial year",
        description="Create a new financial year period. The start date must be before the end date.",
        tags=["financial-years"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a financial year",
        description="Get details of a specific financial year including its date range.",
        tags=["financial-years"]
    ),
    update=extend_schema(
        summary="Update a financial year",
        description="Update the details of an existing financial year. Start date must be before end date.",
        tags=["financial-years"]
    ),
    partial_update=extend_schema(
        summary="Partially update a financial year",
        description="Partially update an existing financial year. Start date must be before end date.",
        tags=["financial-years"]
    ),
    destroy=extend_schema(
        summary="Delete a financial year",
        description="Delete a financial year. Note that this may affect events associated with this financial year.",
        tags=["financial-years"]
    )
)
class FinancialYearViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing financial years.

    Financial years define the accounting periods for organizing
    business transactions and generating financial reports.
    """
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List file attachments",
        description="Retrieve a list of all file attachments associated with accounting events.",
        tags=["attachments"]
    ),
    create=extend_schema(
        summary="Upload a new file attachment",
        description="Upload a file attachment and associate it with an accounting event. Files are automatically renamed with UUIDs.",
        tags=["attachments"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a file attachment",
        description="Get details of a specific file attachment including its download URL and associated event.",
        tags=["attachments"]
    ),
    update=extend_schema(
        summary="Update a file attachment",
        description="Update the details of an existing file attachment, such as changing the associated event.",
        tags=["attachments"]
    ),
    partial_update=extend_schema(
        summary="Partially update a file attachment",
        description="Partially update an existing file attachment, such as changing the associated event.",
        tags=["attachments"]
    ),
    destroy=extend_schema(
        summary="Delete a file attachment",
        description="Delete a file attachment. This will remove the file from storage and the database record.",
        tags=["attachments"]
    )
)
class AttachmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing file attachments.

    Attachments allow users to associate files (receipts, invoices, etc.)
    with accounting events for documentation and audit purposes.
    """
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
