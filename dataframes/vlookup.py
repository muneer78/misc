import polars as pl
from datetime import datetime as dt

current = dt.now().strftime("%Y-%m-%d")

# Read the Excel file into a DataFrame
df1_orig = pl.read_excel(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\Tied at Both Levels (1).xlsx",
    sheet_name="Export",
)

# Read the CSV file into a DataFrame
df2_orig = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\sfdata.csv")

# Cast the cadmoddate and sfmoddate columns as dates
df2_orig = df2_orig.with_columns(
    [
        pl.col("cadmoddate")
        .str.extract(r"(\d{4}-\d{2}-\d{2})")
        .str.strptime(pl.Date, "%Y-%m-%d")
        .alias("cadmoddate"),
        pl.col("sfmoddate")
        .str.extract(r"(\d{4}-\d{2}-\d{2})")
        .str.strptime(pl.Date, "%Y-%m-%d")
        .alias("sfmoddate"),
    ]
)

# Ensure the column names are correct
print("Columns in df1_orig:", df1_orig.columns)
print("Columns in df2_orig:", df2_orig.columns)

# Join the two DataFrames on the specified columns
result = df1_orig.join(df2_orig, on=["caddetailid"], how="inner")

# Select only the specified columns in the result DataFrame
selected_columns = [
    "caddetailid",
    "clientkey",
    "masterclient",
    "clientno",
    "parentclientno",
    "crmacctid",
    "sfmoddate",
    "cadmoddate",
]

filtered_result = result.select(selected_columns)

print(f"Number of records in result: {len(result)}")

name = "cadence-details"

# Save the filtered result to a CSV file
filtered_result.write_csv(
    rf"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\{current}_{name}.csv"
)
