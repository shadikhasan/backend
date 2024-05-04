from rest_framework import generics,status
from rest_framework.permissions import IsAdminUser
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response


class RoleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = RoleSerializer
    #permission_classes = [IsAdminUser]

class PermissionListAPIView(generics.ListCreateAPIView):
    http_method_names = ['get']
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    

    # permission_classes = [IsAdminUser]

class RolePermissionAssignAPIView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = RoleSerializer
    #permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
            group = self.get_object()
            permission_ids = request.data.get('permission_ids', [])
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)
            return Response({'detail': 'Permissions assigned successfully.'}, status=status.HTTP_200_OK)

class GroupPermissionUpdateAPIView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupPermissionSerializer
    allowed_methods = ['PATCH', 'GET', 'DELETE']
    
    
    def get(self, request, *args, **kwargs):
        group = self.get_object()
        permissions = group.permissions.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        group = self.get_object()
        permission_ids = request.data.get('permission_ids', [])
        permissions = Permission.objects.filter(id__in=permission_ids)
        group.permissions.add(*permissions)
        return Response({'detail': 'Permissions updated successfully.'}, status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        permission_id = request.data.get('permission_id')
        if permission_id is None:
            return Response({'detail': 'Permission ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        permission = Permission.objects.filter(id=permission_id).first()
        if permission is None:
            return Response({'detail': 'Permission not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if permission in group.permissions.all():
            group.permissions.remove(permission)
            return Response({'detail': 'Permission removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Permission not found in the group.'}, status=status.HTTP_404_NOT_FOUND)
        
class UserGroupUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserGroupUpdateSerializer  # Define the serializer class

    def update(self, request, *args, **kwargs):
        group_id = self.kwargs.get('group_id')
        user_ids = self.kwargs.get('user_ids')
        group = Group.objects.get(id=group_id)
        users = User.objects.filter(id__in=user_ids)
        for user in users:
            user.groups.add(group)
        return Response({'detail': 'Users assigned to group successfully.'}, status=status.HTTP_200_OK)