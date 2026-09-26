import polars as pl
from rich import print

# Load the CSV files into DataFrames
df1 = pl.read_csv("A_only.csv")
df2 = pl.read_csv("B_only.csv")

# Filter df1
df1 = df1.filter(pl.col("nk_fuelcardid").str.contains("347907"))

# Calculate the max value of col in dataset 1
max_col1_df1 = df1["totalfuelamt"].max()

# Filter df2
df2 = df2.filter(pl.col("Carrier Id").str.contains("347907"))

# Calculate the max value of col in dataset 2
max_col1_df2 = df2["Qty"].max()

# Calculate the difference
difference = max_col1_df1 - max_col1_df2

# Write all calculations to console
print(f"Max value of col1 in dataset 1: {max_col1_df1}")
print(f"Max value of col1 in dataset 2: {max_col1_df2}")
print(f"Difference between max values: {difference}")
