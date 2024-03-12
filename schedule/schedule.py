from icalendar import Calendar, Event
from configparser import ConfigParser
from schedule.lesson.lesson import Lesson
import requests
import json 
import os

class Schedule:
    def __init__(self):
        cal = Calendar()

        config = ConfigParser()
        config.read('./config.ini')

        team_name = config.get('groups', 'team_name')

        cal_description = f'Plan zajęć {team_name}'
        cal.add('prodid', cal_description)
        cal.add('version', '1.0')

        self.cal = cal

    def save_calendar_to_file(self, path='./', filename='example.ics'):
        print(f'Saving calendar to {path+filename}')
        file = open(os.path.join(path, filename), 'wb')
        file.write(self.cal.to_ical())
        file.close()

    def add_lesson(self, lesson_json):
        lesson = Lesson(lesson_json)

        lesson.add_all()

        self.cal.add_component(Event(lesson))

    def add_lessons(self):
        for lesson in self.odd_parsed_json:
            self.add_lesson(lesson)
        for lesson in self.even_parsed_json:
            self.add_lesson(lesson)

    def get_schedule_from_api(self):
        config = ConfigParser()

        config.read('./config.ini')

        base_url = 'https://schedulescraperpw.azurewebsites.net/api/schedule?'
        week_type = 'N'
        url = ''.join([
            base_url,
            f'TeamName={config.get("groups", "team_name")}',
            f'&LabGropName={config.get("groups", "lab_group_name")}',
            f'&ProjGroupName={config.get("groups", "project_group_name")}',
            f'&CompLabGroupName={config.get("groups", "computer_lab_group_name")}',
            f'&WeekType={week_type}'
        ])

        api_response = requests.get(url)
        parsed_json = json.loads(api_response.text)
        self.__check_status_code(api_response)

        self.odd_parsed_json = parsed_json

        week_type = 'P'
        url = ''.join([
            base_url,
            f'TeamName={config.get("groups", "team_name")}',
            f'&LabGropName={config.get("groups", "lab_group_name")}',
            f'&ProjGroupName={config.get("groups", "project_group_name")}',
            f'&CompLabGroupName={config.get("groups", "computer_lab_group_name")}',
            f'&WeekType={week_type}'
        ])
        api_response = requests.get(url)
        parsed_json = json.loads(api_response.text)
        self.__check_status_code(api_response)

        self.even_parsed_json = parsed_json

    def __check_status_code(self, api_response):
        if api_response.status_code == 200:
            print('Connection succesful')
        else:
            print(f'Error, could not connect. Status code {api_response.status_code}')
    


