from django.db import models
from ride.models import Ride

# Create your models here.

class RideEvent(models.Model):
    """
    RideEvent model following the specified schema:
    - id_ride_event: Primary key
    - id_ride: Foreign key referencing Ride(id_ride)
    - description: Description of the ride event
    - created_at: Timestamp of when the event occurred
    """
    
    id_ride_event = models.AutoField(primary_key=True, db_column='id_ride_event')
    id_ride = models.ForeignKey(Ride, on_delete=models.CASCADE, db_column='id_ride')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ride_event'
        verbose_name = 'Ride Event'
        verbose_name_plural = 'Ride Events'
    
    def __str__(self):
        return f"Ride Event #{self.id_ride_event} - {self.description[:50]}"