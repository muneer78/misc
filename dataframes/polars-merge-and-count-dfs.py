import polars as pl

# DS4660


def count_total_rows_and_combine(file_paths, output_file):
    combined_df = pl.concat([pl.read_csv(file_path) for file_path in file_paths])
    total_rows = len(combined_df)
    combined_df.write_csv(output_file)
    return total_rows


def print_results(total_rows, sorted_columns, counts, title):
    print(f"Total rows: {total_rows}")
    print(f"{title}:")
    for column in sorted_columns:
        print(f"{column}: {counts[column]}")
    print()


# Example usage
file_paths1 = [
    "lead_fmcsa_20240621_000.csv",
    "lead_fmcsa_20240624_000.csv",
    "lead_fmcsa_20240625_000.csv",
    "lead_fmcsa_20240626_000.csv",
    "lead_fmcsa_20240627_000.csv",
    "lead_fmcsa_20240628_000.csv",
]  # Add your file paths here
output_file1 = "combinedleads.csv"

total_rows1 = count_total_rows_and_combine(file_paths1, output_file1)

print("Total leads:", total_rows1)

# Read the dataset from a CSV file
df = pl.read_csv("combinedleads.csv")

filtered_df = df.filter(~pl.col("trucknbr").is_null())

filtered_df = df.with_columns(
    [
        pl.col("dot_number__c").cast(pl.Int64),
        pl.col("mc_number__c").cast(pl.Int64),
        pl.col("physphonenbr").cast(pl.Int64),
        pl.col("trucknbr").cast(pl.Int64),
    ]
)

filtered_df.write_csv("finalcombinedleadsfile.csv")

# Calculate the number of records removed
num_records_removed = df.height - filtered_df.height

print("Number of records removed:", num_records_removed)
