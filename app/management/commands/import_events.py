import json
from django.core.management.base import BaseCommand
from models import Event
from datetime import datetime

class Command(BaseCommand):
    help = 'Import events from a JSON file'

    def handle(self, *args, **kwargs):
        # Load the JSON file containing event data
        with open('events.json', 'r') as file:
            data = json.load(file)
            
            for event_data in data:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(event_data['start_date'], '%Y-%m-%dT%H:%M:%S')
                end_date = datetime.strptime(event_data['end_date'], '%Y-%m-%dT%H:%M:%S')

                # Create an Event object and save it to the database
                event = Event(
                    title=event_data['title'],
                    start_date=start_date,
                    end_date=end_date,
                    days=event_data['days']
                )
                event.save()

            self.stdout.write(self.style.SUCCESS('Successfully imported events from JSON file.'))
