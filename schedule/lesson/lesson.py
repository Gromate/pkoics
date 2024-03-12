from icalendar import Event
from datetime import datetime
import pytz

class Lesson(Event):
    def __init__(self, lesson_json):
        self.lesson_json = lesson_json
        
    def add_description(self):
        description = self.lesson_json['eventType']
        self.add('description', description)

    def add_summary(self):
        summary = self.lesson_json['name']
        self.add('summary', summary)

    def add_location(self):
        location = self.lesson_json['location']
        self.add('location', location)
    
    def add_recurrence(self, interval=2, count=3):
        self.add('RRULE', {'FREQ': 'WEEKLY', 'INTERVAL': interval, 'COUNT': count})

    def add_time(self):
        time_range = self.lesson_json['timeRange']
        start_time, end_time = time_range.split('-')

        start_time = start_time.split(':')
        start_time_hours = (int)(start_time[0])
        start_time_minutes = (int)(start_time[1])

        end_time = end_time.split(':')
        end_time_hours = (int)(end_time[0])
        end_time_minutes = (int)(end_time[1])

        timezone = pytz.timezone('Europe/Warsaw')

        self.add('dtstart', datetime(2024, 3, 15, start_time_hours, start_time_minutes, 0, tzinfo=timezone))
        self.add('dtend', datetime(2024, 3, 15, end_time_hours, end_time_minutes, 0, tzinfo=timezone))