from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from geopy.distance import geodesic
from django.db.models.signals import pre_save, post_delete



class SecondaryTransferStation(models.Model):

    STSID = models.AutoField(primary_key=True)
    WardNumber = models.CharField(max_length=20)
    Location = models.CharField(max_length=255)
    #Manager = models.ForeignKey('ecosync.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    Capacity = models.DecimalField(max_digits=10, decimal_places=2)
    Latitude = models.FloatField(default=0.0)  # Default latitude of the GPS coordinates
    Longitude = models.FloatField(default=0.0) 
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.WardNumber
    
class Landfill(models.Model):
    LandfillID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Location = models.CharField(max_length=255)
    #Manager = models.ForeignKey('ecosync.CustomUser', on_delete=models.CASCADE, blank=True, null=True)
    Capacity = models.DecimalField(max_digits=10, decimal_places=2)  # Default capacity of the landfill
    OperationalTimespan = models.CharField(max_length=100, default='24/7')  # Operational timespan of the landfill
    Latitude = models.FloatField(default=0.0)  # Default latitude of the GPS coordinates
    Longitude = models.FloatField(default=0.0)  # Default longitude of the GPS coordinates
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name
    
class Vehicle(models.Model):

    VEHICLE_TYPES = [
        ('Open Truck', 'Open Truck'),
        ('Dump Truck', 'Dump Truck'),
        ('Compactor', 'Compactor'),
        ('Container Carrier', 'Container Carrier'),
    ]
    
    CAPACITY_CHOICES = [
        (3, '3 ton'),
        (5, '5 ton'),
        (7, '7 ton'),
        (15, '15 ton'),  # Adding 15 ton capacity choice
    ]
    
    VehicleID = models.AutoField(primary_key=True)
    RegistrationNumber = models.CharField(max_length=100)
    Type = models.CharField(max_length=255, choices=VEHICLE_TYPES)
    Capacity = models.IntegerField(choices=CAPACITY_CHOICES)  # Changed to IntegerField
    FuelCostLoaded = models.DecimalField(max_digits=10, decimal_places=2)
    FuelCostUnloaded = models.DecimalField(max_digits=10, decimal_places=2)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.RegistrationNumber

class WasteTransfer(models.Model):
    TransferID = models.AutoField(primary_key=True)
    Vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    Source = models.ForeignKey('SecondaryTransferStation', related_name='source_transfer', on_delete=models.CASCADE)
    Destination = models.ForeignKey('Landfill', related_name='destination_transfer', on_delete=models.CASCADE)
    Distance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Distance attribute added
    VolumeOfWaste = models.DecimalField(max_digits=10, decimal_places=2)
    TimeOfArrival = models.DateTimeField()
    TimeOfDeparture = models.DateTimeField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.TransferID:
            # If it's a new transfer, calculate the distance before saving
            self.Distance = self.calculate_distance()
        super().save(*args, **kwargs)

    def calculate_distance(self):
        source_coords = (self.Source.Latitude, self.Source.Longitude)
        destination_coords = (self.Destination.Latitude, self.Destination.Longitude)
        return geodesic(source_coords, destination_coords).kilometers

    
class OilAllocation(models.Model):
    AllocationID = models.AutoField(primary_key=True)
    Vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    WeekNumber = models.IntegerField()
    VolumeOfWaste = models.DecimalField(max_digits=10, decimal_places=2)
    OilAllocated = models.DecimalField(max_digits=10, decimal_places=2)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.OilAllocated)
class Billing(models.Model):
    BillID = models.AutoField(primary_key=True)
    Vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    WeekNumber = models.IntegerField()
    VolumeOfWaste = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='VolumeOfWaste')
    Distance = models.DecimalField(max_digits=10, decimal_places=2)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    
class DumpingEntryRecord(models.Model):
    EntryID = models.AutoField(primary_key=True)
    Vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    Landfill = models.ForeignKey('Landfill', on_delete=models.CASCADE)
    VolumeOfWaste = models.DecimalField(max_digits=10, decimal_places=2)
    TimeOfArrival = models.DateTimeField()
    TimeOfDeparture = models.DateTimeField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    
class Role(models.Model):
    RoleID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.Name



