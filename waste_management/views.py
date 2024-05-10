# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from core.permissions import *
class WasteTransferViewSet(viewsets.ModelViewSet):
    queryset = WasteTransfer.objects.all()
    serializer_class = WasteTransferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wastetransfer = serializer.save()
        return Response(WasteTransferSerializer(wastetransfer).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Customize create logic here if needed
        serializer.save()

class SecondaryTransferStationViewSet(viewsets.ModelViewSet):
    queryset = SecondaryTransferStation.objects.all()
    serializer_class = SecondaryTransferStationSerializer
    #permission_classes = [IsStsManager]
class LandfillViewSet(viewsets.ModelViewSet):
    queryset = Landfill.objects.all()
    serializer_class = LandfillSerializer
    #permission_classes = [IsStsManager]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    #permission_classes = [IsStsManager]
