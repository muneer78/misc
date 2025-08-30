import polars as pl
import glob
import os

# Set the directory and prefix
directory = "/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Downloads"
prefix = "fuel_trans_summ_"

# Find all files starting with the prefix
pattern = os.path.join(directory, f"{prefix}*")
files = glob.glob(pattern)

total_rows = 0

for file_path in files:
    df = pl.read_csv(file_path, ignore_errors=True)
    row_count = len(df)
    print(f"Rows in {os.path.basename(file_path)}: {row_count}")
    total_rows += row_count

print("Total rows in all matching files:", total_rows)
