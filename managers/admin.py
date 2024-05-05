from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import STSManager, LandfillManager

# Define a decorator to prevent adding instances and raise PermissionDenied
def prevent_adding_permission_denied(model_admin):
    # Define a nested function to raise PermissionDenied
    def _prevent_adding(self, request):
        # Raise PermissionDenied with a customized message
        raise PermissionDenied(f"Adding instances of {self.model.__name__} is not allowed.")
    
    # Replace the add_view method with the _prevent_adding function
    model_admin.add_view = _prevent_adding
    return model_admin

# Register STSManager with the admin panel and apply the prevent_adding_permission_denied decorator
@admin.register(STSManager)
@prevent_adding_permission_denied
class STSManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'sts']

    # Override the delete_queryset method to perform custom deletion
    def delete_queryset(self, request, queryset):
        for manager in queryset:
            # Change the related CustomUser's role to "4" (unassigned) before deleting the manager instance
            manager.user.role_id = 4
            manager.user.save()
        super().delete_queryset(request, queryset)
        
        
# Register LandfillManager with the admin panel and apply the prevent_adding_permission_denied decorator
@admin.register(LandfillManager)
@prevent_adding_permission_denied
class LandfillManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'landfill']
    
    # Override the delete_queryset method to perform custom deletion
    def delete_queryset(self, request, queryset):
        for manager in queryset:
            # Change the related CustomUser's role to "4" (unassigned) before deleting the manager instance
            manager.user.role_id = 4
            manager.user.save()
        super().delete_queryset(request, queryset)