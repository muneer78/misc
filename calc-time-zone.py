import datetime
import pytz

# Define time zones and city names
time_zones = [
    ('US/Pacific', 'PST', 'Los Angeles'),
    ('US/Central', 'CST', 'Kansas City'),
    ('US/Eastern', 'EST', 'Montreal, Orlando, and Toronto'),
    ('Europe/Istanbul', '', 'Istanbul'),
    ('Asia/Karachi', '', 'Karachi'),
    ('Asia/Dhaka', '', 'Dhaka'),
    ('Pacific/Tarawa','', 'Tarawa')
]

# Input a specific date and time in the Central US time zone from the terminal
central_tz = pytz.timezone('US/Central')
input_datetime_str = input("Enter the date and time in Central Time (YYYY-MM-DD HH:MM AM/PM): ")
input_datetime = datetime.datetime.strptime(input_datetime_str, '%Y-%m-%d %I:%M %p')
central_time_input = central_tz.localize(input_datetime)

# Get the specified time in the specified time zones
specified_times = []

for tz_name, tz_abbr, city_name in time_zones:
    tz = pytz.timezone(tz_name)

    # Calculate the time in the other time zones based on the input time in Central time zone
    converted_time = central_time_input.astimezone(tz)

    # Determine whether it's DST or ST for US time zones and adjust the abbreviation accordingly
    if tz_name.startswith('US/'):
        is_dst = tz.localize(datetime.datetime(converted_time.year, 3, 8)) <= converted_time <= tz.localize(datetime.datetime(converted_time.year, 11, 1))
        tz_abbr = 'PDT' if is_dst else 'PST' if tz_abbr == 'PST' else 'CDT' if is_dst else 'CST' if tz_abbr == 'CST' else 'EDT' if is_dst else 'EST' if tz_abbr == 'EST' else tz_abbr

    formatted_time = converted_time.strftime('%I:%M%p').lstrip('0')  # Remove leading zeroes

    # Exclude the city name for US time zones
    if tz_name.startswith('US/'):
        specified_times.append(f"{formatted_time} {tz_abbr}")
    else:
        specified_times.append(f"{formatted_time} {city_name}")

# Print the results
formatted_results = ', '.join(specified_times)
print(formatted_results)
