from icalendar import Calendar, Event
from datetime import datetime
import tempfile, os
import pytz

cal = Calendar()
cal.add('prodid', 'MyCal')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Spotkanie 1')
event.add('dtstart', datetime(2024, 3, 15, 10, 0, 0, tzinfo=pytz.utc))
event.add('dtend', datetime(2024, 3, 15, 12, 0, 0, tzinfo=pytz.utc))
event.add('dtstamp', datetime(2024, 3, 15, 10, 0, 0, tzinfo=pytz.utc))

cal.add_component(event)

directory = tempfile.mkdtemp()
f = open(os.path.join(directory, 'example.ics'), 'wb')
f.write(cal.to_ical())
f.close()

print(cal.to_ical().decode("utf-8")) 


