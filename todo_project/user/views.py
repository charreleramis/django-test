from rest_framework import viewsets
from user.models import User
from user.serializers import UserSerializer
from user.permissions import IsAdminRole


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations: list, create, retrieve, update, delete
    Only accessible by users with 'admin' role.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'id_user'