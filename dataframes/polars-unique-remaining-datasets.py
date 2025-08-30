import polars as pl

# Read the dataset from a CSV file
df = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Code\powerbi-rs-remaining.csv")

# Filter for unique dataset_ids
df_unique = df.unique(subset=["dataset_id"])

columns = ["dataset_id", "dataset_name"]

final_df = df_unique.select(columns)

# Print all columns in the output
print(final_df)

# Write the unique dataset to a new CSV file
final_df.write_csv("powerbi-rs-remaining-v2.csv")
