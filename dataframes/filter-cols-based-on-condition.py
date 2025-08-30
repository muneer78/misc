import polars as pl

# Read the CSV file
df = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\pointdist25.csv")

# Drop columns where the string 'Rank', '1', or '3' is in the column name, and drop the 'Season' column
columns_to_drop = [
    col
    for col in df.columns
    if any(substring in col for substring in ["Rank", "1", "3"])
] + ["Season"]
filtered_df = df.drop(columns_to_drop)

# Save the updated DataFrame to a new CSV file
output_file_path = (
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\pointdist25-filtered.csv"
)
filtered_df.write_csv(output_file_path)

print(f"Filtered DataFrame saved to {output_file_path}")
