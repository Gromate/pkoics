from icalendar import Event
from datetime import time, date, datetime, timedelta
from configparser import ConfigParser
import pytz

class Lesson(Event):
    def __init__(self, lesson_json):
        self.lesson_json = lesson_json
    
    def add_all(self):
        #self.add_description()
        self.add_summary()
        self.add_location()
        self.add_recurrence()
        self.add_time()
        
    def add_description(self):
        description = self.lesson_json['eventType']
        self.add('description', description)

    def add_summary(self):
        summary = self.lesson_json['name'] + '(' + self.lesson_json['eventType'] + ')'
        self.add('summary', summary)

    def add_location(self):
        location = self.lesson_json['location']
        self.add('location', location)
    
    def add_recurrence(self, interval=2):
        config = ConfigParser()
        config.read('./config.ini')

        semester_end_date_iso = config.get('time', 'semester_end_date')
        semester_end_date = date.fromisoformat(semester_end_date_iso)

        self.add('RRULE', {'FREQ': 'WEEKLY', 'INTERVAL': interval, 'UNTIL': semester_end_date})

    def add_time(self):
        time_range = self.lesson_json['timeRange']
        start_time_iso, end_time_iso = time_range.split('-')

        start_time = time().fromisoformat(start_time_iso.replace(' ', '0'))
        end_time = time().fromisoformat(end_time_iso.replace(' ', '0'))

        config = ConfigParser()
        config.read('./config.ini')

        semester_start_date_iso = config.get('time', 'semester_start_date').strip()
        semester_start_date = date.fromisoformat(semester_start_date_iso)

        ### day_number from 1-5
        #1 -> Monday
        #5 -> Friday
        day_number = self.lesson_json['dayNr']

        week_modifier = self.__week_type_modifier(self.lesson_json['weekType'])
        modifier = timedelta(days=day_number+week_modifier-1)
        lesson_date = semester_start_date + modifier

        timezone_name = config.get('time', 'timezone')
        timezone = pytz.timezone(timezone_name)

        self.__add_start_datetime(lesson_date, start_time, timezone)
        self.__add_end_datetime(lesson_date, end_time, timezone)

    def __add_start_datetime(self, date, time, timezone):
        self.add('dtstart', datetime(
            date.year, 
            date.month, 
            date.day, 
            time.hour,
            time.minute, 
            0, 
            tzinfo=timezone
        ))

    def __add_end_datetime(self, date, time, timezone):
        self.add('dtend', datetime(
            date.year, 
            date.month, 
            date.day, 
            time.hour,
            time.minute, 
            0, 
            tzinfo=timezone
        ))

    def __week_type_modifier(self, week_type):
        #First week of semester is always odd
        #If week is even it should start 7 days later
        if self.__is_week_even(week_type):
            return 7
        else:
            return 0

    def __is_week_even(self, letter):
        if letter == 'N':
            return False
        elif letter == 'P':
            return True
        else:
            return False
            #raise ValueError('Bad week type identifier')
