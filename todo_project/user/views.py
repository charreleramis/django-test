from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations: list, create, retrieve, update, delete
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


    