import polars as pl

# Read the CSV file into a DataFrame
df = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\large_files.csv")

# Convert the Size column values from bytes to MB and write to a new column called size_in_mb
df = df.with_columns([(pl.col("Size") / (1024 * 1024)).round(2).alias("size_in_mb")])

# Update all headers to lowercase and replace whitespace with dashes
df = df.rename({col: col.lower().replace(" ", "-") for col in df.columns})

df_sorted = df.sort(["size_in_mb"], descending=True)

# Write the updated DataFrame to a new CSV file
df_sorted.write_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\large-files-final.csv"
)

print("Output done")
