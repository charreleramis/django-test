import base64
import json
from datetime import datetime, timedelta
from django.conf import settings


class TokenUtils:
    
    @staticmethod
    def generate_token(user):
        token_data = {
            'email': user.email,
            'role': user.role,
            'id_user': user.id_user,
            'exp': (datetime.now() + timedelta(days=7)).timestamp()
        }
        token_json = json.dumps(token_data)
        token_bytes = token_json.encode('utf-8')
        token = base64.b64encode(token_bytes).decode('utf-8')
        return token
    
    @staticmethod
    def decode_token(token):
        try:
            token_bytes = base64.b64decode(token.encode('utf-8'))
            token_json = token_bytes.decode('utf-8')
            token_data = json.loads(token_json)
            
            if datetime.now().timestamp() > token_data.get('exp', 0):
                return None
            
            return token_data
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            return None
    
    @staticmethod
    def get_user_from_token(token):
        token_data = TokenUtils.decode_token(token)
        if not token_data:
            return None
        
        from user.models import User
        try:
            user = User.objects.get(email=token_data.get('email'))
            return user
        except User.DoesNotExist:
            return None
