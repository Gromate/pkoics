from icalendar import Calendar, Event
from datetime import datetime
from schedule.schedule import Schedule

schedule = Schedule('13K1')
schedule.init_calendar()

schedule.get_schedule_from_api()

schedule.add_lesson()

schedule.save_calendar_to_file()