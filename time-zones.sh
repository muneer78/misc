timezones=("America/Chicago" "Asia/Dhaka" "Asia/Karachi" "Asia/Riyadh")

for tz in "${timezones[@]}"; do
    echo "$tz\t$(TZ=$tz date +%Y-%m-%d' '%H:%M)"
done