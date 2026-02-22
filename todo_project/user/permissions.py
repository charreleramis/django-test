from rest_framework import permissions
from user.models import User


class IsAdminRole(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not isinstance(request.user, User):
            return False
        
        return request.user.role == 'admin'
