from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.token_utils import TokenUtils


class CookieTokenAuthentication(BaseAuthentication):
    """Returns None when no token (used for signin/signup which use AllowAny)."""

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


class RequireCookieTokenAuthentication(BaseAuthentication):
    """Raises 401 when no token or invalid token. Use on views that must not be accessible without auth."""

    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')

        if not token:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Token '):
                token = auth_header.split(' ')[1]

        if not token:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        user = TokenUtils.get_user_from_token(token)

        if not user:
            raise AuthenticationFailed('Invalid or expired token.')

        return (user, None)

    def authenticate_header(self, request):
        return 'Token'


class CookieOnlyAdminAuthentication(BaseAuthentication):
    """
    Auth for protected APIs using the Cookie header. Expects header: Cookie: <token>.
    No Cookie header or invalid token → 401.
    """

    def authenticate(self, request):
        token = request.META.get('HTTP_COOKIE', '').strip()

        if not token:
            raise AuthenticationFailed(
                'Authentication required. Send the token in the Cookie header (e.g. Cookie: <token>).'
            )

        user = TokenUtils.get_user_from_token(token)

        if not user:
            raise AuthenticationFailed('Invalid or expired token.')

        return (user, None)

    def authenticate_header(self, request):
        return 'Cookie'
