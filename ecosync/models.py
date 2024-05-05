from django.db import models
from django.contrib.auth.models import AbstractUser
from featurs.models import Role
from django.contrib.auth.models import Group
from managers.models import *

class CustomUser(AbstractUser):
    
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=4)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role.Name})"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            original_role_id = None
        else:
            original_role_id = CustomUser.objects.get(pk=self.pk).role_id
        super().save(*args, **kwargs)
        if not is_new and self.role_id != original_role_id:
            print("Role changed. Assigning permission group...")
            self.sync_managers_with_role()
            self.assign_permission_group()
            
    def sync_managers_with_role(self):
            for manager_model in [LandfillManager, STSManager]:
                manager_instance = manager_model.objects.filter(user=self).first()
                if manager_instance:
                    manager_instance.delete()

            if self.role_id == 3:
                LandfillManager.objects.create(user=self)
            elif self.role_id == 2:
                STSManager.objects.create(user=self)

    def assign_permission_group(self):
        print("Assigning permission group...")
        if self.role_id == 3:
            group_name = "LandFill Manager Permissions"
            is_staff = True  # Assuming LandFill Managers are staff members
            is_superuser = False
        elif self.role_id == 2:
            group_name = "STS Manager Permissions"
            is_staff = True  # Assuming STS Managers are staff members
            is_superuser = False
        else:
            print("Role does not correspond to any group.")
            return  # Do nothing if the role doesn't correspond to any group

        try:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f"Group '{group_name}' created.")
            else:
                print(f"Group '{group_name}' already exists.")
                
            self.groups.add(group)
            print(f"User {self.username} added to group: {group_name}")
        
        except Exception as e:
            print(f"Error adding user {self.username} to group {group_name}: {e}")
            return

        self.is_staff = is_staff
        self.is_superuser = is_superuser
        self.save()