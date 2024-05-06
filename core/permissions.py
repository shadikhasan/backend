from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        # Raise NotFound exception for anonymous users
        if not request.user.is_authenticated:
            raise NotFound()
        
        # Check if the user is a system admin
        return request.user.role.Name == "System Admin"
class IsStsManager(BasePermission):
    def has_permission(self, request, view):
        # Raise NotFound exception for anonymous users
        if not request.user.is_authenticated:
            raise NotFound()
        
        # Check if the user is a system admin
        return request.user.role.Name == "STS Manager"
class IsLandfillManager(BasePermission):
    def has_permission(self, request, view):
        # Raise NotFound exception for anonymous users
        if not request.user.is_authenticated:
            raise NotFound()
        
        # Check if the user is a system admin
        return request.user.role.Name == "Landfill Manager"