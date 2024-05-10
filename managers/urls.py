from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import STSManagerViewSet, LandfillManagerViewSet, ContractorManagerViewSet

router = DefaultRouter()
router.register(r'sts-managers', STSManagerViewSet)
router.register(r'landfill-managers', LandfillManagerViewSet)
router.register(r'contractor-managers', ContractorManagerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
