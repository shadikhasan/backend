# In your_app/management/commands/initialize_roles.py

from django.core.management.base import BaseCommand
from waste_management.models import Role

class Command(BaseCommand):
    help = 'Initialize roles with initial data'

    def handle(self, *args, **options):
        # Check if there are any existing roles
        existing_roles_count = Role.objects.count()
        if existing_roles_count > 0:
            self.stdout.write(self.style.SUCCESS("Roles already exist. Skipping initialization."))
            return

        initial_roles = [
            {'Name': 'System Admin', 'Description': 'Description of System Admin role'},
            {'Name': 'STS Manager', 'Description': 'Description of STS Manager role'},
            {'Name': 'Landfill Manager', 'Description': 'Description of Landfill Manager role'},
            {'Name': 'Unassigned', 'Description': 'Description of Unassigned role'},
            {'Name': 'Contractor Manager', 'Description': 'Description of Contractor Manager role'},
        ]

        for role_data in initial_roles:
            role, created = Role.objects.get_or_create(Name=role_data['Name'], defaults=role_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Role '{role.Name}' created successfully with ID {role.pk}."))
            else:
                self.stdout.write(self.style.WARNING(f"Role '{role.Name}' already exists."))

        self.stdout.write(self.style.SUCCESS("Roles initialization completed."))
