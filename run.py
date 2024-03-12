from icalendar import Calendar, Event
from datetime import datetime
from schedule.schedule import Schedule

schedule = Schedule()

schedule.get_schedule_from_api()

schedule.add_lessons()

schedule.save_calendar_to_file()