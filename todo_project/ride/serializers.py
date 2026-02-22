from rest_framework import serializers
from ride.models import Ride
from ride_event.serializers import RideEventSerializer
from user.serializers import UserSerializer


class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    ride_events = RideEventSerializer(many=True, read_only=True, source='rideevent_set')
    
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ['id_ride']
