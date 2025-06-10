from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_monitor']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()