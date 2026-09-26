import polars as pl
import os
from datetime import datetime as dt

# DS4209
# Get the current date
current_date = dt.now().strftime("%Y-%m-%d")


def sortvalues(df):
    # Create temporary columns for case-insensitive sorting
    df = df.with_columns(
        [
            pl.col("ext_field").str.to_lowercase().alias("ext_field_lower"),
            pl.col("sf_object").str.to_lowercase().alias("sf_object_lower"),
        ]
    )
    # Sort by these temporary columns
    df = df.sort(["ext_field_lower", "sf_object_lower"])
    # Drop the temporary columns after sorting
    df = df.drop(["ext_field_lower", "sf_object_lower"])
    return df


# Create a mapping for the 'processid' values
processid_mapping = {1: "New", 2: "Update"}

# Default value if the processid is not in the mapping
default_value = "Both"

# Your file path
file = "fieldmapping.csv"

# Get the filename without extension
filename = os.path.splitext(os.path.basename(file))[0]

# Read the CSV file into a Polars DataFrame
dforig = pl.read_csv(file)

# Filter out rows where int_field is 'changetonull', null, or an empty string
dforig = dforig.filter(
    (pl.col("int_field") != "changetonull")
    & pl.col("int_field").is_not_null()
    & (pl.col("int_field") != "")
)

# Group by 'int_field' and 'ext_field', count duplicates, and create a new column 'number'
dforig = dforig.with_columns(
    (pl.col("int_field").cumcount().over(["int_field", "ext_field"]) + 1).alias(
        "number"
    )
)

# Add the 'new_or_update' column based on process ID values using map_dict
df = dforig.with_columns(
    pl.col("processid")
    .map_dict(processid_mapping, default=default_value)
    .alias("new_or_update")
)

# Drop duplicates
df1 = df.unique(subset=["int_field", "ext_field", "new_or_update"])

df1_sorted = sortvalues(df1)

# Save the sorted DataFrame to a new CSV file
df1_sorted.write_csv(f"{filename}_{current_date}_processed.csv")

print("Done")
