# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WasteTransferViewSet

router = DefaultRouter()
router.register(r'wastetransfers', WasteTransferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
