from rest_framework import permissions
from user.models import User


class IsAdminRole(permissions.BasePermission):
    """
    Custom permission to only allow users with 'admin' role to access the API.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has the 'admin' role.
        """
        # Check if user is authenticated
        if not request.user or not isinstance(request.user, User):
            return False
        
        # Check if user has the admin role
        return request.user.role == 'admin'
