from icalendar import Calendar, Event
from datetime import datetime
import requests
import json 
import os
import pytz

class Schedule:
    def __init__(self, team_name):
        self.team_name = team_name

    def init_calendar(self):
        cal = Calendar()

        cal_description = f'Plan zajęć {self.team_name}'
        cal.add('prodid', cal_description)
        cal.add('version', '1.0')

        self.cal = cal

    def save_calendar_to_file(self, path='./', filename='example.ics'):
        print(f'Saving calendar to {path+filename}')
        f = open(os.path.join(path, filename), 'wb')
        f.write(self.cal.to_ical())
        f.close()

    def add_lesson(self):
        event = Event()
        event.add('summary', 'Spotkanie 2')
        event.add('dtstart', datetime(2024, 3, 15, 10, 0, 0, tzinfo=pytz.utc))
        event.add('dtend', datetime(2024, 3, 15, 12, 0, 0, tzinfo=pytz.utc))
        event.add('dtstamp', datetime(2024, 3, 15, 0, 10, 0, tzinfo=pytz.utc))
        event.add('RRULE', {'FREQ': 'WEEKLY', 'INTERVAL': 2, 'COUNT': 3})

        self.cal.add_component(event)

    def get_schedule_from_api(self):
        base_url = 'https://schedulescraperpw.azurewebsites.net/api/schedule?'
        url = ''.join([
            base_url,
            f'TeamName={self.team_name}',
            f'&LabGropName=L01',
            f'&ProjGroupName=P01',
            f'&CompLabGroupName=K01',
            f'&WeekType=P'
        ])

        api_response = requests.get(url)
        parsed_json = json.loads(api_response.text)
        self.__check_status_code(api_response)

        print(parsed_json[0]['name'])

    def __check_status_code(self, api_response):
        if api_response.status_code == 200:
            print('Connection succesful')
        else:
            print(f'Error, could not connect. Status code {api_response.status_code}')


