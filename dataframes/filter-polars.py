import polars as pl
from datetime import date as dt
# Read the dataset from a CSV file
# df1 = pl.read_csv(r'C:\Users\mahmad\OneDrive - Ryan RTS\1- Projects\powerbi-research.csv')

# Read the Excel file
df1 = pl.read_excel(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\1- Projects\powerbi-research-rs-only.xlsx",
    sheet_name="powerbi-research-rs-only",
)

current_date = dt.today()

# Ensure the 'Finished' column is treated as a date
df1 = df1.with_columns(pl.col("Finished").cast(pl.Date))

# Filter the DataFrame by date
df = df1.filter(pl.col("Finished") == pl.lit(f"{current_date}").cast(pl.Date))

# Filter the DataFrame by string
# df = df1.filter(pl.col("RyanTrans") == "y")

# Group by 'dataset_name' and get the number of unique values
df_unique = df.group_by("dataset_name", maintain_order=True).agg(pl.col("*").n_unique())

# Print the result as a list with each item on a new line, prefixed with "* "
unique_list = df_unique.to_series().to_list()
for item in unique_list:
    print(f"* {item}")
