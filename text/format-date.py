from datetime import datetime
import pytz

# Define the timezone
timezone = pytz.timezone("US/Central")

# Get the current time with timezone
date = datetime.now(timezone)

# Format the date to the desired format
formatted_date = date.strftime("%Y-%m-%d %H:%M:%S.%f %z")
# Truncate microseconds to 2 decimal places for seconds
formatted_date = (
    formatted_date[:19]
    + formatted_date[19:22]
    + formatted_date[-5:-2]
    + ":"
    + formatted_date[-2:]
)

print(formatted_date)
