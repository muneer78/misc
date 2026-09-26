import polars as pl


def count_total_rows(file_paths):
    total_rows = 0
    for file_path in file_paths:
        df = pl.read_csv(file_path)
        total_rows += len(df)
    return total_rows


def print_results(total_rows):
    print(f"Total rows: {total_rows}")
    print(f"{title}:")
    for column in sorted_columns:
        print(f"{column}: {counts[column]}")
    print()


# Example usage
file_paths = ["success061324111627065.csv"]  # Add your file paths here
total_rows = count_total_rows(file_paths)

print_results(total_rows)
