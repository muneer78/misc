import polars as pl


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
file_paths = [
    "finalerrorfile_1.csv",
    "finalerrorfile_2.csv",
]  # Add your file paths here
identifier = "carrier_profile_errors"
output_file = f"combined_file_{identifier}.csv"

total_rows = count_total_rows_and_combine(file_paths, output_file)

print("Total records:", total_rows)
