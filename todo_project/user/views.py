from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.models import User
from user.serializers import UserSerializer
from user.permissions import IsAdminRole
from user.services import UserService
from user.token_utils import TokenUtils


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserService.get_base_queryset()
    serializer_class = UserSerializer
    lookup_field = 'id_user'
    permission_classes = [IsAdminRole]
    
    def list(self, request, *args, **kwargs):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
        except (ValueError, TypeError):
            page = 1
            page_size = 10
        
        result = UserService.get_all_users(page=page, page_size=page_size)
        
        data = [user.serialized for user in result['results']]
        
        return Response({
            'count': result['count'],
            'page': result['page'],
            'page_size': result['page_size'],
            'total_pages': result['total_pages'],
            'next': f"?page={page + 1}&page_size={page_size}" if page < result['total_pages'] else None,
            'previous': f"?page={page - 1}&page_size={page_size}" if page > 1 else None,
            'results': data
        })

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def signin(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email:
            return Response({
                'status': 'error',
                'message': 'Email is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({
                'status': 'error',
                'message': 'Password is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = UserService.get_user_by_email(email)
        
        if not user or not user.check_password(password):
            return Response({
                'status': 'error',
                'message': 'Invalid email or password.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        token = TokenUtils.generate_token(user)
        
        response = Response({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'user': user.serialized,
                'token': token
            }
        }, status=status.HTTP_200_OK)
        
        response.set_cookie(
            'auth_token',
            token,
            max_age=7*24*60*60,
            httponly=True,
            samesite='Lax',
            secure=False
        )
        
        return response
    

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def signup(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('phone_number')
        role = request.data.get('role', 'user')
        
        if not email:
            return Response({
                'status': 'error',
                'message': 'Email is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({
                'status': 'error',
                'message': 'Password is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not first_name:
            return Response({
                'status': 'error',
                'message': 'First name is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not last_name:
            return Response({
                'status': 'error',
                'message': 'Last name is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if UserService.check_email_exists(email):
            return Response({
                'status': 'error',
                'message': 'User with this email already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(password) < 6:
            return Response({
                'status': 'error',
                'message': 'Password must be at least 6 characters long.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = UserService.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number or '',
                role=role
            )
            
            token = TokenUtils.generate_token(user)
            
            response = Response({
                'status': 'success',
                'message': 'User created successfully.',
                'data': {
                    'user': user.serialized,
                    'token': token
                }
            }, status=status.HTTP_201_CREATED)
            
            response.set_cookie(
                'auth_token',
                token,
                max_age=7*24*60*60,
                httponly=True,
                samesite='Lax',
                secure=False
            )
            
            return response
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error creating user: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)