import pandas as pd


def align_schemas(dfs):
    # Get all unique column names from all dataframes
    all_columns = set()
    for df in dfs:
        all_columns.update(df.columns)

    # Create a list of columns with their types from all dataframes
    aligned_dfs = []
    for df in dfs:
        for col in all_columns:
            if col not in df.columns:
                # Add missing column with null values
                df[col] = None
        # Ensure columns are in the same order
        df = df[sorted(all_columns)]
        aligned_dfs.append(df)

    return aligned_dfs


def count_total_rows_and_combine(file_paths, output_file):
    dfs = [pd.read_csv(file_path) for file_path in file_paths]
    aligned_dfs = align_schemas(dfs)
    combined_df = pd.concat(aligned_dfs, ignore_index=True)
    total_rows = len(combined_df)
    combined_df.to_csv(output_file, index=False)
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
