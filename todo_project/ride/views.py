from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ride.models import Ride
from ride.serializers import RideSerializer


class RideViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ride model.
    Provides CRUD operations: list, create, retrieve, update, delete
    """
    queryset = Ride.objects.all()
    serializer_class = RideSerializer