from typing import List, Optional
from django.db.models import QuerySet
from user.models import User


class UserService:
    
    @staticmethod
    def get_base_queryset() -> QuerySet:
        return User.objects.all()
    
    @staticmethod
    def get_all_users(page: int = 1, page_size: int = 20) -> dict:
        offset = (page - 1) * page_size
        queryset = User.objects.all().order_by('-id_user')
        
        total_count = queryset.count()
        users = list(queryset[offset:offset + page_size])
        
        return {
            'results': users,
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size if total_count > 0 else 0
        }
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        try:
            return User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def check_email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists()
    
    @staticmethod
    def get_users_by_role(role: str = None) -> List[User]:
        queryset = User.objects.all()
        if role:
            queryset = queryset.filter(role=role)
        return list(queryset)
    
    @staticmethod
    def create_user(email: str, password: str, first_name: str, last_name: str, 
                   phone_number: str = '', role: str = 'user') -> User:
        user = User(
            email=email,
            password='',
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number or '',
            role=role
        )
        user.set_password(password)
        user.save()
        return user
