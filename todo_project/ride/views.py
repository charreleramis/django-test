from rest_framework import viewsets
from ride.models import Ride
from ride.serializers import RideSerializer
from user.permissions import IsAdminRole


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id_ride'