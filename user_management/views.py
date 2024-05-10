# ecosync/views.py
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from rest_framework.views import APIView
from core.permissions import IsSystemAdmin
from .serializers import *
from profile_management.serializers import *

class CustomUserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete', 'patch']  # Include 'patch' in the allowed methods
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsSystemAdmin]

    def update(self, request, *args, **kwargs):
        if not request.user.role.Name == "System Admin":
            return Response({"detail": "You don't have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Use partial=True for PATCH
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        # Hash the password before saving
        hashed_password = make_password(self.request.data.get('password'))
        serializer.save(password=hashed_password)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)  # For PATCH, just call the update method
    
class AuthCreateViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsSystemAdmin]


class UserRolesViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put']  # Only allow GET and PUT requests
    permission_classes = [IsSystemAdmin]
    serializer_class = UserRoleSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})  # Passing request to context
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if not request.user.role.Name == "System Admin":  # Check if the user is a system admin
            return Response({"detail": "You don't have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        serializer = UpdateProfileSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    


class UserRolesListViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Role.objects.all()
    serializer_class = UserRoleListSerializer
    #permission_classes = [IsSystemAdmin]
