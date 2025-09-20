from rest_framework import viewsets
from .models import Event, FinancialYear
from .serializers import EventSerializer, FinancialYearSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class FinancialYearViewSet(viewsets.ModelViewSet):
    queryset = FinancialYear.objects.all()
    serializer_class = FinancialYearSerializer
