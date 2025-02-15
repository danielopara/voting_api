from .models import AppUser, User
from django.core.exceptions import ValidationError
from rest_framework import serializers
import random
from voting_api.utils import create_unique_id

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs={
            'password': {'write_only': True},
            'email': {'required': True}
        }
        
    def create(self, validated_data):
        return User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username=validated_data['email'],
            email = validated_data['email'],
            password= validated_data['password']
        )
        
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    
class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = AppUser
        fields = ('usr_id','full_name', 'user' )
        read_only_fields = ('usr_id', 'full_name')
            
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        id = create_unique_id("USR", AppUser, "usr_id")
        return AppUser.objects.create(
            usr_id = id,
            user = user,
            full_name = f"{user.first_name} {user.last_name}"
        )
        