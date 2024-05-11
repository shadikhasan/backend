# views.py
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from core.models import CustomUser
from waste_management.models import Role
from .models import *
from rest_framework import viewsets

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Assign role for normal citizen
            role, _ = Role.objects.get_or_create(Name='Normal Citizen')
            user = serializer.save(role=role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueReportCreateView(generics.CreateAPIView):
    queryset = IssueReport.objects.all()
    serializer_class = IssueReportSerializer
    # permission_classes = [IsAuthenticated]
    
    
class PublicNotificationViewSet(viewsets.ModelViewSet):
    queryset = PublicNotification.objects.all()
    serializer_class = PublicNotificationSerializer
    
    
class VolunteerRegistrationCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VolunteerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)