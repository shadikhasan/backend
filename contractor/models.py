from django.db import models
from waste_management.models import Area, SecondaryTransferStation


class ThirdPartyContractor(models.Model):
    name = models.CharField(max_length=100)
    contract_id = models.CharField(max_length=50, unique=True)
    reg_id = models.CharField(max_length=50)
    reg_date = models.DateField()
    tin = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    workforce_size = models.PositiveIntegerField()
    payment_per_ton = models.DecimalField(max_digits=10, decimal_places=2)
    waste_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    contract_duration = models.DurationField()
    area_of_collection = models.ForeignKey(Area, related_name='collection_contractors', on_delete=models.CASCADE)
    designated_sts = models.ForeignKey(SecondaryTransferStation, related_name='sts_contractors', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
