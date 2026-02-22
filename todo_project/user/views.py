from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.models import User
from user.serializers import UserSerializer
from user.permissions import IsAdminRole
from user.services import UserService


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserService.get_base_queryset()
    serializer_class = UserSerializer
    lookup_field = 'id_user'
    permission_classes=[AllowAny]

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
        
        return Response({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'user': user.serialized,
                'token': user.serialized.email
            }
        }, status=status.HTTP_200_OK)
    

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
            
            return Response({
                'status': 'success',
                'message': 'User created successfully.',
                'data': user.serialized
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Error creating user: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)