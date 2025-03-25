import polars as pl
from rich import print
from datetime import datetime as dt
import ast

# Get the current date
current_date = dt.now().strftime("%Y%m%d")

df = pl.read_csv(r"/Users/muneer78/Downloads/rankings2025.csv")

# Count the number of occurrences of each value in the acctexec column and sort by count
grouped_df = (
    df.group_by("Team")
    .agg(pl.col("Team").count().alias("count"))
    .sort("count", descending=True)
)

# Print the resulting DataFrame
print(grouped_df)

name = 'baseball'

# ticket_number = '4530'
output_filename = fr"/Users/muneer78/Downloads/{current_date}_{name}_pivot.csv"

# Save the resulting DataFrame to a CSV file
grouped_df.write_csv(output_filename)

print(f"Data saved to {output_filename} successfully!")