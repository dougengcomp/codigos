from ics import Calendar, Event
from datetime import datetime, timedelta

# Create a new calendar
cal = Calendar()

# Starting date: 21st October 2024 (13:45)
start_date = datetime(2024, 10, 21, 13, 45)
duration = timedelta(minutes=10)  # Each event lasts for 10 minutes

# List of sublist links (from sublist 2 to sublist 10)
sublists = [
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist02",
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist03",
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist04",
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist05",
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist06",
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist07",
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist08",
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist09",
    "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist10"
]

# Create events for each sublist
for i, link in enumerate(sublists):
    event = Event()
    event.name = f"Study AWL Sublist {i+2}"
    event.begin = start_date + timedelta(days=i)  # Each day at 13:45
    event.duration = duration
    event.description = f"Link: {link}"
    cal.events.add(event)

# Save the calendar to a .ics file
with open("awl_study_schedule.ics", 'w') as f:
    f.writelines(cal)

print("ICS file created: awl_study_schedule.ics")
