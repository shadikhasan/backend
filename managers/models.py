from django.db import models
from waste_management.models import *

class STSManager(models.Model):
    user = models.OneToOneField('core.CustomUser', on_delete=models.CASCADE, unique=True)  # Ensure uniqueness of user
    sts = models.ForeignKey(SecondaryTransferStation, on_delete=models.CASCADE, related_name='managers', null= True, blank=True)

    def __str__(self):
        return self.user.username
    
    def delete(self, *args, **kwargs):
        # Change the related CustomUser's role to "4" (unassigned) before deleting the manager instance
        self.user.role_id = 4
        self.user.save()
        super().delete(*args, **kwargs)

class LandfillManager(models.Model):
    user = models.OneToOneField('core.CustomUser', on_delete=models.CASCADE, unique=True)  # Ensure uniqueness of user
    landfill = models.ForeignKey(Landfill, on_delete=models.CASCADE, related_name='managers', null = True, blank = True)

    def __str__(self):
        return self.user.username
    
    def delete(self, *args, **kwargs):
        # Change the related CustomUser's role to "4" (unassigned) before deleting the manager instance
        self.user.role_id = 4
        self.user.save()
        super().delete(*args, **kwargs)
