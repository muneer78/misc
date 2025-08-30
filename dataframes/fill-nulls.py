import polars as pl

# Read the dataset from a CSV file, ensuring all columns are read and empty values are handled
df = pl.read_csv(
    r"/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Downloads/national-origins.csv"
)

# Fill null values with "null" in the "LanguageInSalesforce" column
updated_df = df.with_columns(
    [
        pl.col("LanguageInSalesforce").fill_null("null"),
    ]
)

# Write the entire DataFrame back to a new CSV file
updated_df.write_csv(
    r"/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Downloads/national-origins-updated.csv"
)

print("Null values in 'LanguageInSalesforce' column filled and saved to new CSV file.")
