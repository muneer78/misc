import polars as pl

df = pl.read_excel(r"/Users/muneer78/Downloads/vinyl.xlsx")

df.write_csv(r"/Users/muneer78/Downloads/vinyl.csv")

print("Excel file converted to CSV file successfully!")