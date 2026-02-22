from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
import base64


class CustomUserAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Basic '):
            return None
        
        try:
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            email, password = decoded_credentials.split(':', 1)
            
            try:
                user = User.objects.get(email=email)
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
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Token '):
            return None
        
        try:
            token = auth_header.split(' ')[1]
            user = User.objects.get(email=token)
            return (user, None)
        except (User.DoesNotExist, IndexError):
            return None
    
    def authenticate_header(self, request):
        return 'Token'
