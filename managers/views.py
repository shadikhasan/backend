from rest_framework import viewsets
from .models import STSManager, LandfillManager, ContractorManager
from .serializers import STSManagerSerializer, LandfillManagerSerializer, ContractorManagerSerializer
from core.permissions import *
class STSManagerViewSet(viewsets.ModelViewSet):
    queryset = STSManager.objects.all()
    serializer_class = STSManagerSerializer
    #permission_classes = [IsSystemAdmin]

class LandfillManagerViewSet(viewsets.ModelViewSet):
    queryset = LandfillManager.objects.all()
    serializer_class = LandfillManagerSerializer
    #permission_classes = [IsSystemAdmin]

class ContractorManagerViewSet(viewsets.ModelViewSet):
    queryset = ContractorManager.objects.all()
    serializer_class = ContractorManagerSerializer
    #permission_classes = [IsSystemAdmin]
