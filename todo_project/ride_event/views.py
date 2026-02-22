from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ride_event.models import RideEvent
from ride_event.serializers import RideEventSerializer


class RideEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RideEvent model.
    Provides CRUD operations: list, create, retrieve, update, delete
    """
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
