import polars as pl
from rich import print


def load_data(file_path):
    return pl.read_csv(file_path)


def count_total_rows(df):
    return len(df)


def count_exit_in_column(df):
    exit_counts = {
        column: df.select(
            pl.col(column)
            .cast(pl.Utf8)
            .str.to_lowercase()
            .str.count_matches("exit", literal=True)
        )
        .sum()
        .item()
        for column in df.columns
    }
    return exit_counts


def sort_columns_by_occurrences(counts):
    return sorted(counts, key=counts.get, reverse=True)


def calculate_differences(counts1, counts2, columns):
    return {
        column: counts2.get(column, 0) - counts1.get(column, 0) for column in columns
    }


def print_results(total_rows, sorted_columns, counts, title):
    print(f"Total rows: {total_rows}")
    print(f"{title}:")
    for column in sorted_columns:
        print(f"{column}: {counts[column]}")
    print()


def print_differences(differences, sorted_columns_diff):
    print("Difference in counts in old vs new dataset:")
    for column in sorted_columns_diff:
        print(f"{column}: {differences[column]}")


# Load datasets
df1 = load_data("cadence_20240503_182156000.csv")
df2 = load_data("CadenceSalesforceActiveInactiveCriteria.csv")

# Count total rows in each DataFrame
total_rows_df1 = count_total_rows(df1)
total_rows_df2 = count_total_rows(df2)

# Count occurrences of 'exit' in each column
count_df1 = count_exit_in_column(df1)
count_df2 = count_exit_in_column(df2)

# Sort columns by the number of occurrences of 'exit'
sorted_df1 = sort_columns_by_occurrences(count_df1)
sorted_df2 = sort_columns_by_occurrences(count_df2)

# Calculate differences in counts between old and new datasets
differences = calculate_differences(count_df1, count_df2, df1.columns)

# Sort columns by the differences in counts
sorted_columns_diff = sorted(
    df1.columns, key=lambda column: differences[column], reverse=False
)

# Print results
print_results(
    total_rows_df1,
    sorted_df1,
    count_df1,
    "Sorted column order by number of 'exit' occurrences in old dataset",
)
print_results(
    total_rows_df2,
    sorted_df2,
    count_df2,
    "Sorted column order by number of 'exit' occurrences in new dataset",
)
print_differences(differences, sorted_columns_diff)
