from django.db import models

# Create your models here.

class User(models.Model):
    """
    User model following the specified schema:
    - id_user: Primary key
    - role: User role ('admin' or other roles)
    - first_name: User's first name
    - last_name: User's last name
    - email: User's email address
    - phone_number: User's phone number
    """
    
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
    
    class Meta:
        db_table = 'user'  # Optional: specify table name
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"