from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Basic serializer for User model."""
    
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id_user']
        extra_kwargs = {
            'password': {'write_only': True}  # Password should not be returned in responses
        }
    
    def create(self, validated_data):
        """Override create to hash password."""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """Override update to hash password if provided."""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
