import polars as pl
from rich import print

# Read the CSV file into a DataFrame
df = pl.read_csv("fieldmapping.csv")

# Filter df
df = df.filter(pl.col("sf_object").str.contains("account"))

# Get the total number of rows
total_rows = df.select(pl.len())

print(total_rows)
