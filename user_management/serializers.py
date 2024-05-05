# ecosync/serializers.py

from rest_framework.serializers import ModelSerializer
from core.models import CustomUser
from rest_framework import serializers
from waste_management.models import Role
class CustomUserSerializer(ModelSerializer):
    role_name = serializers.CharField(source='role.Name', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username','first_name', 'last_name', 'email', 'role', 'role_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserRoleSerializer(ModelSerializer):
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['role', 'role_name']

    def get_role_name(self, obj):
        return obj.role.Name if obj.role else None

class UserRoleListSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ['RoleID', 'Name', 'Description']


