# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import WasteTransfer
from .serializers import WasteTransferSerializer

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
