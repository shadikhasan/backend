from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from geopy.distance import geodesic
from django.db.models.signals import pre_save, post_delete



class Area(models.Model):
    ZONE_CHOICES = [
        (1, 'Zone 1'),
        (2, 'Zone 2'),
        (3, 'Zone 3'),
        (4, 'Zone 4'),
        (5, 'Zone 5'),
    ]
    zone = models.IntegerField(choices=ZONE_CHOICES, primary_key=True)

    def __str__(self) -> str:
        return str(self.zone)
class SecondaryTransferStation(models.Model):

    STSID = models.AutoField(primary_key=True)
    WardNumber = models.CharField(max_length=20)
    Location = models.CharField(max_length=255)
    Capacity = models.DecimalField(max_digits=10, decimal_places=2)
    Latitude = models.FloatField(default=0.0)  # Default latitude of the GPS coordinates
    Longitude = models.FloatField(default=0.0) 
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    fine_for_compensation = models.DecimalField(max_digits=10, decimal_places=2, default=500)  # New field for fine
    collection_hours = models.CharField(max_length=100, default="08:00-17:00")  # New Field for Collection hours
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        # return self.WardNumber 
        return f"{self.WardNumber} ({self.Location})"
    
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



    
class DumpingEntryRecord(models.Model):
    EntryID = models.AutoField(primary_key=True)
    Vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    SecondaryTransferStation = models.ForeignKey('SecondaryTransferStation', on_delete=models.CASCADE, default=3)
    Landfill = models.ForeignKey('Landfill', on_delete=models.CASCADE)
    VolumeOfWaste = models.DecimalField(max_digits=10, decimal_places=2)
    Distance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    TimeOfArrival = models.DateTimeField(blank=True, null=True)
    TimeOfDeparture = models.DateTimeField(blank=True, null=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dumping Entry / Oill Allocation(Billing)"
        verbose_name_plural = "Dumping Entrys / Oill Allocations (Billings)"

    
class Role(models.Model):
    RoleID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.Name



