from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import *
from rest_framework.views import APIView
from core.permissions import IsSystemAdmin
from .serializers import *

class ProfileViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch']  # Only allow GET and PUT requests
    serializer_class = ProfileSerializer
    queryset = CustomUser.objects.all()
    #permission_classes = [IsSystemAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = CustomUser.objects.filter(pk=self.request.user.pk)
        return queryset

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance, context={'request': request})  # Passing request to context
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance, data=request.data, context={'request': request})  # Passing request to context
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
