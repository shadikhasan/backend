# views.py=
from rest_framework import viewsets
from core.permissions import *
from waste_management.models import SecondaryTransferStation, Landfill, Vehicle, WasteTransfer, DumpingEntryRecord
from .serializers import SecondaryTransferStationSerializer, LandfillSerializer, VehicleSerializer, WasteTransferSerializer, DumpingEntryRecordSerializer

class SecondaryTransferStationViewSet(viewsets.ModelViewSet):
    queryset = SecondaryTransferStation.objects.all()
    serializer_class = SecondaryTransferStationSerializer
    #permission_classes = [IsSystemAdmin]
    
class LandfillViewSet(viewsets.ModelViewSet):
    queryset = Landfill.objects.all()
    serializer_class = LandfillSerializer
    permission_classes = [IsSystemAdmin]
    
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsSystemAdmin]
    
class WasteTransferViewSet(viewsets.ModelViewSet):
    queryset = WasteTransfer.objects.all()
    serializer_class = WasteTransferSerializer
    permission_classes = [IsStsManager]
    
class DumpingEntryRecordViewSet(viewsets.ModelViewSet):
    queryset = DumpingEntryRecord.objects.all()
    serializer_class = DumpingEntryRecordSerializer
    permission_classes = [IsLandfillManager]