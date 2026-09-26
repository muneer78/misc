import polars as pl

# Read the Excel file
df1 = pl.read_excel(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\Marketing Cloud Data Research.xlsx",
    sheet_name="Fields, Use Cases, Sources",
)

# Apply the formula logic to filter the DataFrame
df = df1.filter(
    # (pl.col("Status") == "validate fields")
    # & (
    pl.any_horizontal(
        pl.col("Marketing Data Source").cast(pl.Utf8).str.contains("(?i)RTS Pro")
        # | pl.col("Actual Data Source").is_null()
        # | pl.col("Actual Data Source").str.strip_chars().str.contains("^$")
    )
)
# )
# Print the number of rows in the filtered DataFrame
print("Rows:", len(df))

# Save the updated DataFrame back to a CSV file
df.write_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\6304-rts-pro.csv")
