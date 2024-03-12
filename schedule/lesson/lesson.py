from icalendar import Event
from datetime import time, date, datetime
from configparser import ConfigParser
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
        start_time_iso, end_time_iso = time_range.split('-')

        start_time = time().fromisoformat(start_time_iso)
        end_time = time().fromisoformat(end_time_iso)

        config = ConfigParser()
        config.read('./config.ini')

        semester_start_date_iso = config.get('time', 'semester_start_date')
        semester_start_date = date.fromisoformat(semester_start_date_iso)

        timezone_name = config.get('time', 'timezone')
        timezone = pytz.timezone(timezone_name)

        self.add_start_datetime(semester_start_date, start_time, timezone)
        self.add_end_datetime(semester_start_date, end_time, timezone)

    def add_start_datetime(self, date, time, timezone):
        self.add('dtstart', datetime(
            date.year, 
            date.month, 
            date.day, 
            time.hour,
            time.minute, 
            0, 
            tzinfo=timezone
        ))

    def add_end_datetime(self, date, time, timezone):
        self.add('dtstart', datetime(
            date.year, 
            date.month, 
            date.day, 
            time.hour,
            time.minute, 
            0, 
            tzinfo=timezone
        ))
