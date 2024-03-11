from icalendar import Calendar, Event
from datetime import datetime
from configparser import ConfigParser
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
        file = open(os.path.join(path, filename), 'wb')
        file.write(self.cal.to_ical())
        file.close()

    def add_lesson(self):
        event = Event()
        lesson_number = 3
        event.add('summary', self.schedule_json[lesson_number]['name'])

        description = self.schedule_json[lesson_number]['eventType']
        location = self.schedule_json[lesson_number]['location']
        time_range = self.schedule_json[lesson_number]['timeRange']

        start_time, end_time = time_range.split('-')
        start_time = start_time.split(':')
        end_time = end_time.split(':')

        event.add('dtstart', datetime(2024, 3, 15, (int)(start_time[0]), (int)(start_time[1]), 0, tzinfo=pytz.utc))
        event.add('dtend', datetime(2024, 3, 15, (int)(end_time[0]), (int)(end_time[1]), 0, tzinfo=pytz.utc))
        event.add('location', location)
        event.add('description', description)
        event.add('RRULE', {'FREQ': 'WEEKLY', 'INTERVAL': 2, 'COUNT': 3})

        self.cal.add_component(event)

    def get_schedule_from_api(self):
        config = ConfigParser()

        config.read('./config.ini')

        base_url = 'https://schedulescraperpw.azurewebsites.net/api/schedule?'
        url = ''.join([
            base_url,
            f'TeamName={config.get("groups", "team_name")}',
            f'&LabGropName={config.get("groups", "lab_group_name")}',
            f'&ProjGroupName={config.get("groups", "project_group_name")}',
            f'&CompLabGroupName={config.get("groups", "computer_lab_group_name")}',
            f'&WeekType=P'
        ])

        api_response = requests.get(url)
        parsed_json = json.loads(api_response.text)
        self.__check_status_code(api_response)

        self.schedule_json = parsed_json

    def __check_status_code(self, api_response):
        if api_response.status_code == 200:
            print('Connection succesful')
        else:
            print(f'Error, could not connect. Status code {api_response.status_code}')


