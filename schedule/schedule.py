from icalendar import Calendar, Event
import os

class Schedule:
    def __init__(self, team_name):
        self.team_name = team_name

    def init_calendar(self):
        cal = Calendar()
        cal.add('prodid', 'MyCal')
        cal.add('version', '1.0')
        self.cal = cal

    def save_calendar_to_file(self, path='./', filename='example.ics'):
        f = open(os.path.join(path, filename), 'wb')
        f.write(self.cal.to_ical())
        f.close()

