from django.core.management.base import BaseCommand
import csv
import os
from django.conf import settings
from store_monitor.models import Store, BusinessHours, StoreStatus

class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    def handle(self, *args, **kwargs):

        # Absolute paths for your CSV files (modify this as needed)
        timezone_csv_path = 'loop_monitor/data/timezone.csv'
        business_hours_csv_path = 'loop_monitor/data/business_hours.csv'
        store_status_csv_path = 'loop_monitor/data/store_status.csv'

        # Import Store timezone CSV
        with open(timezone_csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                _, created = Store.objects.get_or_create(
                    store_id=row[0],
                    defaults={'timezone_str': row[1]}
                )

        # Import BusinessHours CSV
        with open(business_hours_csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                try:
                    store = Store.objects.get(store_id=row[0])
                    _, created = BusinessHours.objects.get_or_create(
                        store=store,
                        day_of_week=row[1],
                        defaults={
                            'start_time_local': row[2],
                            'end_time_local': row[3]
                        }
                    )
                except Store.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Store with id {row[0]} not found in the database. Skipping the entry."))
                    continue

        # Import StoreStatus CSV
        with open(store_status_csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                try:
                    store = Store.objects.get(store_id=row[0])
                    _, created = StoreStatus.objects.get_or_create(
                        store=store,
                        timestamp_utc=row[1],
                        defaults={'status': row[2]}
                    )
                except Store.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Store with id {row[0]} not found in the database. Skipping the entry."))
                    continue

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
