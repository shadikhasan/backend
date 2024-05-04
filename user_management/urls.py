from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from .views import *

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

# users_router = NestedSimpleRouter(router, r'users', lookup='user')
# users_router.register(r'roles', UserRolesViewSet, basename='user-roles')

urlpatterns = [
    path('users/roles/', UserRolesListViewSet.as_view(({'get': 'list'})), name='user-roles-list'),
    path('users/<int:pk>/roles/', UserRolesViewSet.as_view({'put': 'update'}), name='update-user-roles'),
]


urlpatterns += router.urls 