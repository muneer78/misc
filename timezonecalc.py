import datetime
import pytz

# Define time zones and city names
time_zones = [
    ('US/Pacific', 'PST', 'Los Angeles'),
    ('US/Central', 'CST', 'Kansas City'),
    ('US/Eastern', 'EST', 'Montreal, Orlando, and Toronto'),
    ('Europe/Istanbul', '', 'Istanbul'),
    ('Asia/Karachi', '', 'Karachi'),
    ('Asia/Dhaka', '', 'Dhaka')
]

# Get current time in the specified time zones
current_times = []
current_statuses = []

for tz_name, tz_abbr, city_name in time_zones:
    tz = pytz.timezone(tz_name)
    current_time = datetime.datetime.now(tz)
    formatted_time = current_time.strftime('%I:%M%p').lstrip('0')  # Remove leading zeroes

    # Determine whether it's DST or ST for US time zones
    if tz_name.startswith('US/'):
        is_dst = tz.localize(datetime.datetime(current_time.year, 3, 8)) <= current_time <= tz.localize(datetime.datetime(current_time.year, 11, 1))
        dst_status = 'DST' if is_dst else 'ST'
    else:
        dst_status = ''

    current_times.append(formatted_time)
    current_statuses.append(dst_status)

# Print the results
formatted_results = ', '.join([f"{city_name} time: {time} {tz_abbr}" if tz_abbr else f"{city_name} time: {time}" for (_, tz_abbr, city_name), time, status in zip(time_zones, current_times, current_statuses)])
print(formatted_results)
