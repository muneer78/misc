import polars as pl
import csv
from datetime import datetime as dt

# Get the current date
current_date = dt.now()

# Load the CSV files using Polars
df1 = pl.read_csv("file1.csv")
df2 = pl.read_csv("file2.csv")


# Define the xlookup function using Polars' filtering capabilities
def xlookup(lookup_value, lookup_array, return_array, if_not_found: str = None):
    match_value = return_array.filter(lookup_array == lookup_value)
    if match_value.is_empty():
        return if_not_found
    else:
        return match_value[0]


# Perform single column lookup and update 'col3'
lookup_values = df1["col1"]
lookup_array = df2["col1"]
return_array = df2["col3"]

# Apply the xlookup function to each value in lookup_values
lookup_results = [xlookup(val, lookup_array, return_array) for val in lookup_values]

# Add the results as a new column in df1
df1 = df1.with_columns(pl.Series(name="col4", values=lookup_results))

# Select only the required columns
columns = ["col1"]

# Drop duplicates based on the specified columns
df1 = df1.unique(subset=columns)

ticket_number = "insert Jira number here"
output_filename = f"DS{ticket_number}_{current_date}_output.csv"

# Write to CSV, skipping rows where 'col3' is null
with open(output_filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    for row in df1.iter_rows(named=True):
        if row["col1"] is None:
            continue  # skip row if col3 is null

        writer.writerow([row[col] for col in columns])

print("Job done")
