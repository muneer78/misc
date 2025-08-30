import polars as pl

# Sample data
df = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\Book1.csv")

# Split the text_column into multiple columns
split_df = df.with_columns(
    pl.col("error_message").str.split(": ").alias("split_column")
)

# Expand the split_column into separate columns
expanded_df = split_df.with_columns(
    [
        pl.col("split_column")
        .arr.eval(pl.element().alias(f"col_{i + 1}"))
        .arr.explode()
        for i in range(2)
    ]
).drop("split_column")

# Save the resulting DataFrame to a CSV file
expanded_df.write_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\split.csv")

print("Split columns saved to split.csv")
