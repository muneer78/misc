import polars as pl
from datetime import datetime as dt

# Get the current date
current_date = dt.now()

# Sample data
df = pl.DataFrame(
    {"text_column": ["John, Doe, 30", "Jane, Smith, 25", "Alice, Johnson, 40"]}
)

# Split the text_column into multiple columns
split_df = df.with_columns(pl.col("text_column").str.split(", ").alias("split_column"))

# Expand the split_column into separate columns
expanded_df = split_df.with_columns(
    [pl.col("split_column").arr.get(i).alias(f"col_{i + 1}") for i in range(3)]
).drop("split_column")

ticket_number = "insert Jira number here"
output_filename = f"DS{ticket_number}_{current_date}_output.csv"

# Save the resulting DataFrame to a CSV file
split_df.write_csv(output_filename)
