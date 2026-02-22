from rest_framework import viewsets
from ride_event.models import RideEvent
from ride_event.serializers import RideEventSerializer
from user.permissions import IsAdminRole


class RideEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RideEvent model.
    Provides CRUD operations: list, create, retrieve, update, delete
    Only accessible by users with 'admin' role.
    """
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id_ride_event'