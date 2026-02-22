from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Basic serializer for User model."""
    
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id_user']
