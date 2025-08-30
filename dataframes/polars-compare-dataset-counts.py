import polars as pl
from rich import print

# Load the CSV files using Polars
df1 = pl.read_csv("A_only.csv")
df2 = pl.read_csv("B_only.csv")

# Count the number of records in each dataframe
count_df1 = df1.height
count_df2 = df2.height

# Calculate the difference in counts
difference = count_df1 - count_df2

# Print the counts and the difference
print(f"Count of dataset 1: {count_df1}")
print(f"Count of dataset 2: {count_df2}")
print(f"Difference in counts: {difference}")
