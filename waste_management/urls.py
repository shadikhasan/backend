# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'wastetransfers', WasteTransferViewSet)
router.register(r'sts', SecondaryTransferStationViewSet)
router.register(r'landfills', LandfillViewSet)
router.register(r'vehicles', VehicleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
