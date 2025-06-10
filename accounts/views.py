from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    RegisterSerializer, UserSerializer, PasswordChangeSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer, UserProfileSerializer
)
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import generics
from .tasks import send_email_task

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            
            code = get_random_string(length=6, allowed_chars='0123456789')
            user.profile_code = code
            user.save()
            
            subject = 'Password Change Verification'
            message = f'Your verification code is: {code}'
            send_email_task.delay(subject, message, user.email)
            
            return Response({'message': 'Verification code sent to email'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeConfirmView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.profile_code != serializer.validated_data['code']:
                return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.profile_code = None
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                code = get_random_string(length=6, allowed_chars='0123456789')
                user.profile_code = code
                user.save()
                
                subject = 'Password Reset Verification'
                message = f'Your verification code is: {code}'
                send_email_task.delay(subject, message, user.email)
                
                return Response({'message': 'Verification code sent to email'})
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user and user.profile_code == serializer.validated_data['code']:
                user.set_password(serializer.validated_data['new_password'])
                user.profile_code = None
                user.save()
                return Response({'message': 'Password reset successfully'})
            return Response({'error': 'Invalid email or code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user