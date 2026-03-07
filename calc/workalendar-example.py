from workalendar.usa import UnitedStates
from datetime import date, timedelta

cal = UnitedStates()

d = date(2026, 7, 1)
next_working = cal.add_working_days(d, 10)
print(next_working)