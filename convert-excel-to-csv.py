import polars as pl

df = pl.read_excel(r"/Users/muneer78/Downloads/rankings2025.xlsx")

df.write_csv(r"/Users/muneer78/Downloads/rankings2025.csv")

print("Excel file converted to CSV file successfully!")