from datetime import datetime
from zoneinfo import ZoneInfo

TIME_ZONES = {
    "Los Angeles": "America/Los_Angeles",
    "Kansas City": "America/Chicago",
    "Orlando & Toronto": "America/New_York",
    "Istanbul": "Europe/Istanbul",
    "Riyadh": "Asia/Riyadh",
    "Khartoum": "Africa/Khartoum",
    "Karachi": "Asia/Karachi",
}

date_string = input(
    "Enter the date and time in Central Time (YYYY-MM-DD HH:MM): "
)

central_time = datetime.strptime(
    date_string, "%Y-%m-%d %H:%M"
).replace(tzinfo=ZoneInfo("America/Chicago"))

central_offset = central_time.utcoffset()

for city, zone_name in TIME_ZONES.items():
    converted_time = central_time.astimezone(ZoneInfo(zone_name))
    difference = (converted_time.utcoffset() - central_offset).total_seconds() / 3600

    if difference > 0:
        comparison = f"{difference:g} hours ahead"
    elif difference < 0:
        comparison = f"{abs(difference):g} hours behind"
    else:
        comparison = "same time"

    formatted_time = converted_time.strftime("%I:%M %p").lstrip("0")
    print(f"{city}: {formatted_time} ({comparison})")
