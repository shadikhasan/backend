from django.db import models
from featurs.models import *
from ecosync.models import *

# STS Manager Model
class STSManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    sts = models.ForeignKey(SecondaryTransferStation, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return self.user.username

# Landfill Manager Model
class LandfillManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    landfill = models.ForeignKey(Landfill, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return self.user.username
