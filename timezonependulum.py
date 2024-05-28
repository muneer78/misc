import pendulum

central_tz = pendulum.timezone("US/Central")

time_zones = {
    "PT": "US/Pacific",
    "CT": "US/Central",
    "ET": "US/Eastern",
    "Istanbul": "Europe/Istanbul",
    "Karachi": "Asia/Karachi",
    "Dhaka": "Asia/Dhaka",
    "Tarawa": "Pacific/Tarawa"
}

input_str = input("Enter the date and time in Central Time (YYYY-MM-DD HH:MM AM/PM): ")
input_dt = pendulum.from_format(input_str, "YYYY-MM-DD hh:mm A", tz=central_tz)

output = []
for tz_abbr, tz_name in time_zones.items():
    tz = pendulum.timezone(tz_name)
    dt = input_dt.in_timezone(tz)

    if tz_abbr in ["PT", "CT", "ET"]:
        output.append("{} {}".format(dt.format("h:mmA"), tz_abbr))
    else:
        output.append("{} {}".format(dt.format("h:mmA"), tz_name.split("/")[-1]))

print(", ".join(output))
