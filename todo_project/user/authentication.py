from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.token_utils import TokenUtils


class CookieTokenAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')
        
        if not token:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Token '):
                token = auth_header.split(' ')[1]
            else:
                return None
        
        user = TokenUtils.get_user_from_token(token)
        
        if not user:
            return None
        
        return (user, None)
    
    def authenticate_header(self, request):
        return 'Token'
