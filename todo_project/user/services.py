from typing import List, Optional
from django.db import connection
from django.db.models import QuerySet
from user.models import User


class UserService:
    
    @staticmethod
    def get_base_queryset() -> QuerySet:
        return User.objects.all()
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        query = "SELECT id_user FROM user WHERE email = %s LIMIT 1"
        with connection.cursor() as cursor:
            cursor.execute(query, [email])
            row = cursor.fetchone()
            if row:
                user_id = row[0]
                return User.objects.get(id_user=user_id)
            return None
    
    @staticmethod
    def check_email_exists(email: str) -> bool:
        query = "SELECT COUNT(*) FROM user WHERE email = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [email])
            count = cursor.fetchone()[0]
            return count > 0
    
    @staticmethod
    def get_users_by_role(role: str = None) -> List[User]:
        if role:
            query = "SELECT id_user FROM user WHERE role = %s"
            params = [role]
        else:
            query = "SELECT id_user FROM user"
            params = []
        
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            user_ids = [row[0] for row in cursor.fetchall()]
            
            if not user_ids:
                return []
            
            return list(User.objects.filter(id_user__in=user_ids))
    
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
        
        query = """
            INSERT INTO user (email, password, first_name, last_name, phone_number, role)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [
                user.email,
                user.password,
                user.first_name,
                user.last_name,
                user.phone_number,
                user.role
            ])
            user_id = cursor.lastrowid
        
        return User.objects.get(id_user=user_id)
