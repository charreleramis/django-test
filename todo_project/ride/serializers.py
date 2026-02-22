from rest_framework import serializers
from ride.models import Ride


class RideSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ['id_ride']
