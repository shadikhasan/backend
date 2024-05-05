# your_app/management/commands/create_demo_data.py

import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone
from waste_management.models import SecondaryTransferStation, Landfill, Vehicle, WasteTransfer, OilAllocation, Billing, DumpingEntryRecord

fake = Faker()

class Command(BaseCommand):
    help = 'Creates demo data for testing purposes'

    def handle(self, *args, **options):
        self.create_secondary_transfer_stations()
        self.create_landfills()
        self.create_vehicles()
        self.create_waste_transfers()
        self.create_oil_allocations()
        self.create_billings()
        self.create_dumping_entry_records()

    def create_secondary_transfer_stations(self):
        for _ in range(5):
            SecondaryTransferStation.objects.create(
                WardNumber=fake.random_int(min=1, max=20),
                Location=fake.address(),
                Capacity=random.uniform(100, 1000),
                Latitude=fake.latitude(),
                Longitude=fake.longitude(),
            )

    def create_landfills(self):
        for _ in range(3):
            Landfill.objects.create(
                Name=fake.company(),
                Location=fake.address(),
                Capacity=random.uniform(1000, 5000),
                OperationalTimespan='24/7',
                Latitude=fake.latitude(),
                Longitude=fake.longitude(),
            )

    def create_vehicles(self):
        vehicle_types = ['Open Truck', 'Dump Truck', 'Compactor', 'Container Carrier']
        for _ in range(10):
            Vehicle.objects.create(
                RegistrationNumber=fake.license_plate(),
                Type=random.choice(vehicle_types),
                Capacity=random.choice([3, 5, 7, 15]),
                FuelCostLoaded=random.uniform(50, 200),
                FuelCostUnloaded=random.uniform(50, 200),
            )

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

    def create_oil_allocations(self):
        vehicles = Vehicle.objects.all()
        for _ in range(10):
            OilAllocation.objects.create(
                Vehicle=random.choice(vehicles),
                WeekNumber=fake.random_int(min=1, max=52),
                VolumeOfWaste=random.uniform(1, 20),
                OilAllocated=random.uniform(50, 200),
            )

    def create_billings(self):
        vehicles = Vehicle.objects.all()
        for _ in range(10):
            Billing.objects.create(
                Vehicle=random.choice(vehicles),
                WeekNumber=fake.random_int(min=1, max=52),
                VolumeOfWaste=random.uniform(1, 20),
                Distance=random.uniform(10, 100),
            )

    def create_dumping_entry_records(self):
        vehicles = Vehicle.objects.all()
        landfills = Landfill.objects.all()
        for _ in range(20):
            DumpingEntryRecord.objects.create(
                Vehicle=random.choice(vehicles),
                Landfill=random.choice(landfills),
                VolumeOfWaste=random.uniform(1, 20),
                TimeOfArrival=timezone.now(),
                TimeOfDeparture=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS('Demo data created successfully!'))
