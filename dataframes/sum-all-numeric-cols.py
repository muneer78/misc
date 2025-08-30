import polars as pl

df = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\algo.csv")

# Add a new column that contains the sum of all numeric columns for each row
df_add = df.with_columns(
    pl.sum_horizontal(
        [pl.col(col) for col in df.columns if df[col].dtype in [pl.Float64, pl.Int64]]
    )
    .alias("total")
    .round(1)
)

df_add.write_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\algo_filtered.csv"
)  # Save the modified DataFrame to a new CSV file
print("Job done")
