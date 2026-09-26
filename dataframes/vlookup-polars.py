import polars as pl
from datetime import datetime as dt

# Get the current date
current_date = dt.now()

# Read the CSV files
df1 = pl.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Code\powerbi-research-rework.csv"
)
df2 = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Code\rs_unique.csv")

# Rename the column in df2 to match df1
df2 = df2.rename({"dataset": "dataset_id"})

# Perform the join
result = df1.join(df2, on="dataset_id", how="left")

# Select all columns from df1 and specific columns from df2
selected_columns = df1.columns + ["isredshift"]

# Select the specified columns
result = result.select(selected_columns)

# # Convert 'Last View Date' to datetime with the correct format
# result = result.with_columns(pl.col("Last View Date").str.strptime(pl.Date, "%m/%d/%Y"))

# Sort by dataset_id and 'Last View Date'
result = result.sort("Sort", "Views (L90D)", descending=[False, True])

# Drop duplicates keeping the most recent record for each dataset_id
# result_most_recent = result.unique(keep="last")
# Get the rows with the maximum 'Views (L90D)' for each 'dataset_id'
# max_views = result.group_by("dataset_id").agg(pl.col("Views (L90D)").max())

# Join back with the original DataFrame to get the complete rows
# result_highest = result.join(
#     max_views, on=["dataset_id", "Views (L90D)"], how="left"
# )


# Define the output filename
# ticket_number = "5121"
# output_filename = f"DS{ticket_number}_{current_date.strftime('%m%d%Y')}_merged_v5.csv"

# Print the result
print(result)

# Write the result to a CSV file
result.write_csv("new-pbi-research.csv")
