import polars as pl

# Define parameters
down_payment = 28000
buy_initial_payment = 1435
buy_annual_increase = 0.05
rent_initial_payment = 860
rent_annual_increase = 0.09

# Define the number of months to consider
months = 360  # 30 years

# Create a dataframe for months
df = pl.DataFrame({"month": range(1, months + 1)})

# Calculate the monthly payment for buying and renting
df = df.with_columns(
    [
        (
            (
                buy_initial_payment
                * ((1 + buy_annual_increase) ** ((pl.col("month") - 1) // 12))
            ).alias("buy_monthly_payment")
        ),
        (
            (
                rent_initial_payment
                * ((1 + rent_annual_increase) ** ((pl.col("month") - 1) // 12))
            ).alias("rent_monthly_payment")
        ),
    ]
)

# Calculate the cumulative cost for buying and renting
df = df.with_columns(
    [
        (
            pl.col("buy_monthly_payment").cum_sum().alias("buy_cumulative_payment")
            + down_payment
        ),
        (pl.col("rent_monthly_payment").cum_sum().alias("rent_cumulative_payment")),
    ]
)

# Find the point where buying becomes cheaper than renting
result = df.filter(
    pl.col("buy_cumulative_payment") <= pl.col("rent_cumulative_payment")
).select(["month", "buy_cumulative_payment", "rent_cumulative_payment"])

# Convert the month number to years and months
if result.height > 0:
    months_passed = result[0, "month"]
    years = months_passed // 12
    months = months_passed % 12
    print(
        f"Buying becomes cheaper than renting after {years} years and {months} months."
    )
else:
    print("Buying never becomes cheaper than renting within the given timeframe.")
