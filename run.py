from icalendar import Calendar, Event
from datetime import datetime
import tempfile, os
import requests
import json 
import pytz

url = 'https://schedulescraperpw.azurewebsites.net/api/schedule?TeamName=13K1&LabGropName=L01&ProjGroupName=P01&CompLabGroupName=K01&WeekType=P'

api_response = requests.get(url)
if api_response.status_code == 200:
    print('Success')
parsed_json = json.loads(api_response.text)

print(parsed_json[0]['name'])

cal = Calendar()
cal.add('prodid', 'MyCal')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Spotkanie 1')
event.add('dtstart', datetime(2024, 3, 15, 10, 0, 0, tzinfo=pytz.utc))
event.add('dtend', datetime(2024, 3, 15, 12, 0, 0, tzinfo=pytz.utc))
event.add('dtstamp', datetime(2024, 3, 15, 0, 10, 0, tzinfo=pytz.utc))
event.add('RRULE', {'FREQ': 'WEEKLY', 'INTERVAL': 2, 'COUNT': 3})

cal.add_component(event)

path = r"./"
filename = r"example.ics"

f = open(os.path.join(path, filename), 'wb')
f.write(cal.to_ical())
f.close()


