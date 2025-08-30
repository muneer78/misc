import polars as pl
from rich import print
from datetime import datetime as dt
import ast

# Get the current date
current_date = dt.now()

df = pl.read_csv("finalerrorfile_1.csv")


# Extract portion of string in field
def extract_status_code(json_str):
    parsed_list = ast.literal_eval(json_str)
    return parsed_list[0]["statusCode"]


# Create new column
df = df.with_columns(
    pl.col("SalesforceResponse_errors").apply(extract_status_code).alias("statusCode")
)

# Count the number of occurrences of each value in the acctexec column and sort by count
grouped_df = (
    df.group_by("statusCode")
    .agg(pl.col("statusCode").count().alias("count"))
    .sort("statusCode", descending=True)
)

# Print the resulting DataFrame
print(grouped_df)

# ticket_number = '4530'
# output_filename = f"DS{ticket_number}_{current_date}_output.csv"
output_filename = "20240822CarrierProfileErrors.csv"

# Save the resulting DataFrame to a CSV file
grouped_df.write_csv(output_filename)
