import polars as pl

# Read Excel file
df = pl.read_csv("dataloadtestdata.csv")

# Get unique values from the "Bundle Type" column
unique_bundle_types = df["Bundle Type"].unique()

# Create separate dataframes for each unique bundle type and write to CSV
for bundle_type in unique_bundle_types:
    temp_df = df.filter((df["Bundle Type"] == bundle_type))
    if temp_df.height > 0:  # Check if dataframe is not empty
        csv_file_name = f"DS4000-{bundle_type}.csv"
        temp_df.write_csv(csv_file_name)

print("All done")
