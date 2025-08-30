import polars as pl
from datetime import datetime as dt
from datetime import timedelta
import holidays

date_today = dt.now()

# Define US holidays
us_holidays = holidays.country_holidays("US")


# Function to count business days excluding holidays
def business_days_excluding_holidays(start_date, end_date, holidays):
    total_days = (end_date - start_date).days + 1
    business_days = sum(
        1
        for day in (start_date + timedelta(n) for n in range(total_days))
        if day.weekday() < 5 and day not in holidays
    )
    return business_days


# Create a DataFrame with single date
df = pl.DataFrame({"start": [date_today], "end": [dt(2024, 10, 20)]})

# # Create a DataFrame with multiple dates
# df = pl.DataFrame({
#         "start": [date(2020, 1, 1), date(2020, 1, 2)],
#         "end": [date(2020, 1, 2), date(2020, 1, 10)]})

# Apply the function to calculate business days excluding holidays
updated_df = df.with_columns(
    pl.struct(["start", "end"])
    .map_elements(
        lambda row: business_days_excluding_holidays(
            row["start"], row["end"], us_holidays
        )
    )
    .alias("working_day_count")
)

print(updated_df)
