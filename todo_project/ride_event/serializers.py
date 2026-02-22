from rest_framework import serializers
from ride_event.models import RideEvent


class RideEventSerializer(serializers.ModelSerializer):
    """Basic serializer for RideEvent model."""
    
    class Meta:
        model = RideEvent
        fields = '__all__'
        read_only_fields = ['id_ride_event', 'created_at']
