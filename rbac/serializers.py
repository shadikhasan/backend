from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from core.models import CustomUser as User
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')
        
class GroupPermissionSerializer(serializers.ModelSerializer):
    permission_ids = serializers.ListField(child=serializers.IntegerField(), required=True)

    class Meta:
        model = Group
        fields = ('id', 'permission_ids')
        
class UserGroupUpdateSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
