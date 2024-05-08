from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from waste_management.models import Role
from managers.models import LandfillManager, STSManager

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role.Name})"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if not is_new:
            original_role_id = CustomUser.objects.get(pk=self.pk).role_id
        else:
            original_role_id = None

        super().save(*args, **kwargs)

        if not is_new and self.role_id != original_role_id:
            print("Role changed. Assigning permission group...")
            self.sync_managers_with_role()
            self.assign_permission_group()

    def sync_managers_with_role(self):
        # Delete existing manager instance
        LandfillManager.objects.filter(user=self).delete()
        STSManager.objects.filter(user=self).delete()

        # Create new manager based on role
        if self.role_id == 3:
            LandfillManager.objects.create(user=self)
        elif self.role_id == 2:
            STSManager.objects.create(user=self)

    def assign_permission_group(self):
        print("Assigning permission group...")
        
        # Clear all existing groups
        self.groups.clear()

        if self.role_id is None:
            print("User is unassigned. No permissions assigned.")
            self.is_staff = False
            self.is_superuser = False
            self.save()
            return

        if self.role_id == 4:
            print("User role is '4'. Removing from all groups.")
            self.is_staff = False
            self.is_superuser = False
            self.save()
            return

        is_staff = False
        is_superuser = False

        if self.role_id == 1:
            print("User role is 'System Admin'. Assigning system admin permissions.")
            is_staff = True
            is_superuser = True
        elif self.role_id == 2:
            group_name = "STS Manager Permissions"
            is_staff = True
        elif self.role_id == 3:
            group_name = "Landfill Manager Permissions"
            is_staff = True

        # Attempt to get the group or create it if it doesn't exist
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Group '{group_name}' created.")
        else:
            print(f"Group '{group_name}' already exists.")
        
        # Add user to the group
        self.groups.add(group)  # Add the user to the group
        
        print(f"User {self.username} added to group: {group_name}")

        # Set user attributes
        self.is_staff = is_staff
        self.is_superuser = is_superuser
        self.save()
