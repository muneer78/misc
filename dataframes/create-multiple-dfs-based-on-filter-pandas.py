import pandas as pd

df = pd.read_excel(
    "20231103FuelBundles.xlsx",
    sheet_name="Sheet1",
)


# Get unique values from the "Bundle Type" column
unique_bundle_types = df["Bundle Type"].unique()

# Create separate dataframes for each unique bundle type
bundle_type_dataframes = {}
for bundle_type in unique_bundle_types:
    temp_df = df[(df["Bundle Type"] == bundle_type) & (df["DataLoad"] == "Y")]
    if not temp_df.empty:
        bundle_type_dataframes[bundle_type] = temp_df

# Write each dataframe to a CSV file
for bundle_type, df in bundle_type_dataframes.items():
    csv_file_name = f"SAL7467FuelBundle-{bundle_type}.csv"
    df.to_csv(csv_file_name, index=False)

print("All done")
