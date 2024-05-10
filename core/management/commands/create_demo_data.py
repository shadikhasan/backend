from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from waste_management.models import SecondaryTransferStation, Landfill, Vehicle, WasteTransfer, DumpingEntryRecord

fake = Faker()

class Command(BaseCommand):
    help = 'Creates demo data for testing purposes'

    def handle(self, *args, **options):
        self.create_secondary_transfer_stations()
        self.create_landfills()
        self.create_vehicles()
        self.create_waste_transfers()
        self.create_dumping_entry_records()
        self.stdout.write(self.style.SUCCESS('Demo data created successfully!'))

    def create_secondary_transfer_stations(self):
        for _ in range(5):
            station = SecondaryTransferStation.objects.create(
                WardNumber=fake.random_int(min=1, max=20),
                Location=fake.address(),
                Capacity=random.uniform(100, 1000),
                Latitude=fake.latitude(),
                Longitude=fake.longitude(),
                area_id=random.randint(1, 5)  # Assigning a random area ID
            )
            station.save()

    def create_landfills(self):
        for _ in range(3):
            landfill = Landfill.objects.create(
                Name=fake.company(),
                Location=fake.address(),
                Capacity=random.uniform(1000, 5000),
                OperationalTimespan='24/7',
                Latitude=fake.latitude(),
                Longitude=fake.longitude(),
            )
            landfill.save()

    def create_vehicles(self):
        vehicle_types = ['Open Truck', 'Dump Truck', 'Compactor', 'Container Carrier']
        for _ in range(10):
            vehicle = Vehicle.objects.create(
                RegistrationNumber=fake.license_plate(),
                Type=random.choice(vehicle_types),
                Capacity=random.choice([3, 5, 7, 15]),
                FuelCostLoaded=random.uniform(50, 200),
                FuelCostUnloaded=random.uniform(50, 200),
            )
            vehicle.save()

    def create_waste_transfers(self):
        vehicles = Vehicle.objects.all()
        stations = SecondaryTransferStation.objects.all()
        landfills = Landfill.objects.all()
        for _ in range(20):
            transfer = WasteTransfer.objects.create(
                Vehicle=random.choice(vehicles),
                Source=random.choice(stations),
                Destination=random.choice(landfills),
                VolumeOfWaste=random.uniform(1, 20),
                TimeOfArrival=timezone.now(),
                TimeOfDeparture=timezone.now(),
            )
            transfer.save()

    def create_dumping_entry_records(self):
        vehicles = Vehicle.objects.all()
        landfills = Landfill.objects.all()
        for _ in range(20):
            record = DumpingEntryRecord.objects.create(
                Vehicle=random.choice(vehicles),
                Landfill=random.choice(landfills),
                VolumeOfWaste=random.uniform(1, 20),
                TimeOfArrival=timezone.now(),
                TimeOfDeparture=timezone.now(),
            )
            record.save()
