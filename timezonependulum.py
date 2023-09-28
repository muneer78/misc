import pendulum

# Define time zones and city names
time_zones = [
    ("PST", "Los Angeles"),
    ("CST", "Kansas City"),
    ("EST", "Montreal, Orlando, and Toronto"),
    ("Europe/Istanbul", "Istanbul"),
    ("Asia/Karachi", "Karachi"),
    ("Asia/Dhaka", "Dhaka"),
]

us_tz_map = {
    "PST": "America/Los_Angeles",
    "CST": "America/Chicago",
    "EST": "America/New_York",
}

# Input datetime in Chicago time
input_datetime = pendulum.from_format(
    input("Enter the date and time in Central Time (YYYY-MM-DD HH:MM AM/PM): "),
    "YYYY-MM-DD hh:mm A",
)
central_time_input = input_datetime.in_timezone("America/Chicago")

# Get the specified time in the specified time zones
specified_times = []
for tz_abbr, city_name in time_zones:
    if tz_abbr in us_tz_map:
        tz = pendulum.timezone(us_tz_map[tz_abbr])
    else:
        tz = pendulum.timezone(tz_abbr)

    converted_time = central_time_input.in_timezone(tz)
    formatted_time = converted_time.format("h:mmA")

    if tz_abbr in ["PST", "CST", "EST"]:
        specified_times.append(f"{formatted_time} {tz_abbr}")
    else:
        specified_times.append(f"{formatted_time} {city_name}")

# Print results
print(", ".join(specified_times))
