from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('driver', 'Driver'),
        ('passenger', 'Passenger'),
    ]
    
    id_user = models.AutoField(primary_key=True, db_column='id_user')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"