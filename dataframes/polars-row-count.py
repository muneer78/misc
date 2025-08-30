import polars as pl

file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\projects\rpl_account-20250417-Redshift_Prod.csv"

df = pl.read_csv(file_path, ignore_errors=True)

total_rows = len(df)

print("Total rows in file:", total_rows)
