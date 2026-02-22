from django.db import models
from user.models import User

# Create your models here.

class Ride(models.Model):
    """
    Ride model following the specified schema:
    - id_ride: Primary key
    - status: Ride status (e.g., 'en-route', 'pickup', 'dropoff')
    - id_rider: Foreign key referencing User(id_user)
    - id_driver: Foreign key referencing User(id_user)
    - pickup_latitude: Latitude of pickup location
    - pickup_longitude: Longitude of pickup location
    - dropoff_latitude: Latitude of dropoff location
    - dropoff_longitude: Longitude of dropoff location
    - pickup_time: Pickup time
    """
    
    STATUS_CHOICES = [
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id_ride = models.AutoField(primary_key=True, db_column='id_ride')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='en-route')
    id_rider = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_rider')
    id_driver = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_driver')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()
    
    class Meta:
        db_table = 'ride'
        verbose_name = 'Ride'
        verbose_name_plural = 'Rides'
    
    def __str__(self):
        return f"Ride #{self.id_ride} - {self.status} (Rider: {self.id_rider}, Driver: {self.id_driver})"