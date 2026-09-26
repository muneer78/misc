import polars as pl
import os
from datetime import datetime as dt

# SAL8959

# Get the current date
current_date = dt.now().strftime(
    "%Y%m%d"
)  # Format the date to avoid invalid characters

# Your file path
file = "DS3928-20240624.csv"

filename = os.path.splitext(os.path.basename(file))[0]

# Read the CSV file
dforig = pl.read_csv(file)

# Convert the 'createddate' column to datetime
df = dforig.with_columns(pl.col("createddate").str.to_datetime("%Y-%m-%d %H:%M:%S.%f"))

# Add a new column with the formatted date
df = df.with_columns(
    pl.col("createddate").dt.strftime("%Y-%m-%d").alias("formatted_createddate")
)

# Drop the original 'createddate' column
df = df.drop("createddate")

# Filter rows where 'formatted_createddate' is greater than '2024-04-01'
df_filtered = df.filter("formatted_createddate" > "2024-02-01")

# Sort by the new formatted date column
df_sorted = df_filtered.sort(["formatted_createddate"], descending=True)

# Write the sorted DataFrame to a new CSV file
df_sorted.write_csv("20240624ContractIssues.csv")

print("Done")
