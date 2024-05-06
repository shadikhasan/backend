# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SecondaryTransferStationViewSet, LandfillViewSet, VehicleViewSet, WasteTransferViewSet, DumpingEntryRecordViewSet

router = DefaultRouter()
router.register(r'secondary-transfer-stations', SecondaryTransferStationViewSet)
router.register(r'landfills', LandfillViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'waste-transfers', WasteTransferViewSet)
router.register(r'dumping-entries', DumpingEntryRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
