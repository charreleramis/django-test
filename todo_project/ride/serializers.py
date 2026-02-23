from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from ride.models import Ride
from ride_event.serializers import RideEventSerializer
from user.serializers import UserSerializer


class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()
    
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ['id_ride']
    
    def get_todays_ride_events(self, obj):
        if hasattr(obj, 'todays_events'):
            todays_events = obj.todays_events
        else:
            yesterday = timezone.now() - timedelta(hours=24)
            todays_events = obj.rideevent_set.filter(created_at__gte=yesterday).order_by('created_at')
        return RideEventSerializer(todays_events, many=True).data