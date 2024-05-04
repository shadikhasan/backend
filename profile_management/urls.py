from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

# Create a DefaultRouter instance
router = DefaultRouter()
# Register your viewset with the router
router.register(r'profile', ProfileViewSet, basename='profile')

# Add the urlpatterns for the router
urlpatterns = router.urls
