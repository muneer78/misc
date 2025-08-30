import polars as pl

# Define the path to the CSV file
csv_file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\algo.csv"

# Read the CSV file
df = pl.read_csv(csv_file_path)

# Drop rows where the 'seed' column is null
df = df.filter(pl.col("seed").is_not_null())

# Save the updated DataFrame to a new CSV file
output_file_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\algo_filtered.csv"
df.write_csv(output_file_path)

print(f"Filtered CSV saved to {output_file_path}")
