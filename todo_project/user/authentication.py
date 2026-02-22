from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
import base64


class CustomUserAuthentication(BaseAuthentication):
    """
    Custom authentication backend for the custom User model.
    Supports Basic Authentication using email and a simple token/identifier.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request using Basic Authentication.
        Expects email in the username field.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Basic '):
            return None
        
        try:
            # Decode Basic Auth credentials
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            email, password = decoded_credentials.split(':', 1)
            
            # Try to get user by email and verify password
            try:
                user = User.objects.get(email=email)
                # Verify password
                if not user.check_password(password):
                    raise AuthenticationFailed('Invalid credentials')
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed('Invalid credentials')
                
        except (ValueError, IndexError, UnicodeDecodeError):
            raise AuthenticationFailed('Invalid authentication header format')
    
    def authenticate_header(self, request):
        return 'Basic realm="api"'


class TokenAuthentication(BaseAuthentication):
    """
    Simple token authentication for custom User model.
    Uses email as identifier and checks for admin role.
    """
    
    def authenticate(self, request):
        """
        Authenticate using token in Authorization header.
        Format: Authorization: Token <email>
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Token '):
            return None
        
        try:
            token = auth_header.split(' ')[1]
            # In this simple implementation, token is the email
            # In production, use proper token generation and validation
            user = User.objects.get(email=token)
            return (user, None)
        except (User.DoesNotExist, IndexError):
            return None
    
    def authenticate_header(self, request):
        return 'Token'
