from django.urls import path
from .views import *

urlpatterns = [
    path('rbac/roles/', RoleListCreateAPIView.as_view(), name='rbac-role-list-create'),
    path('rbac/permissions/', PermissionListAPIView.as_view(), name='rbac-permission-list-create'),
    path('rbac/roles/<int:pk>/permissions/', RolePermissionAssignAPIView.as_view(), name='rbac-role-permission-assign'),

    path('rbac/groups/<int:pk>/permissions/', GroupPermissionUpdateAPIView.as_view(), name='rbac-group-permissions-update'),

    path('groups/<int:group_id>/assign-users/<user_ids>/', UserGroupUpdateAPIView.as_view(), name='assign-users-to-group'),


]