# myapp/management/commands/load_landfill_data.py
import pandas as pd
from django.core.management.base import BaseCommand
from waste_management.models import Landfill

class Command(BaseCommand):
    help = 'Load data from CSV file to Landfill model'

    def handle(self, *args, **options):
        csv_file = 'data/landfill_data.csv'  # Update the path to your CSV file

        try:
            df = pd.read_csv(csv_file)

            # Check if data exists in the model
            if Landfill.objects.exists():
                self.stdout.write(self.style.WARNING('Data already exists. No changes made.'))
                return

            # Create objects from DataFrame and bulk create them
            objs = [
                Landfill(
                    Name=row['Location'],  # Assuming Location from CSV corresponds to Name in Landfill model
                    Location=row['Location'],
                    Capacity=row['Capacity'],
                    Latitude=row['Latitude'],
                    Longitude=row['Longitude']
                )
                for index, row in df.iterrows()
            ]
            Landfill.objects.bulk_create(objs)

            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))
