import polars as pl

# Sample DataFrame
df = pl.DataFrame({"date_str": ["2023-01-01", "2023-02-01", "2023-03-01"]})

# Convert column 'date_str' from string to date
df = df.with_columns(pl.col("date_str").str.strptime(pl.Date, "%Y-%m-%d"))

print(df)
