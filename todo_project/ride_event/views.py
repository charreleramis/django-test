from rest_framework import viewsets
from ride_event.models import RideEvent
from ride_event.serializers import RideEventSerializer
from user.permissions import IsAdminRole


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id_ride_event'