from icalendar import Calendar, Event
from configparser import ConfigParser
from schedule.lesson.lesson import Lesson
import requests
import json 
import os

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

    def add_lesson(self, lesson_json=None):
        lesson_json = self.schedule_json[10]
        lesson = Lesson(lesson_json)

        lesson.add_all()

        self.cal.add_component(Event(lesson))

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


