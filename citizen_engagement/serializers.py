# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from core.models import CustomUser
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Incorrect username or password")
        return user

class IssueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueReport
        fields = ['location', 'issue_type', 'description', 'anonymous']

class PublicNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicNotification
        fields = '__all__'
        
        
class VolunteerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerRegistration
        fields = '__all__'