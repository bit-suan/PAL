from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Log, Todo

User= get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
            model = User
            fields = ['username', 'email', 'password']
            extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
         user = User.objects.create_user(**validated_data)
         return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['id', 'username', 'email']
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
class LogSerializer(serializers.ModelSerializer):
     class Meta:
          model= Log
          fields= '__all__'
          read_only_fields= ['user', 'date']
    
class TodoSerializer(serializers.ModelSerializer):
     class Meta:
          model= Todo
          fields= '__all__'
          read_only_fields= ['user']

