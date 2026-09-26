import polars as pl
from rich import print


def load_data(file_path):
    return pl.read_csv(file_path)


def count_total_rows(df):
    return len(df)


def sort_columns_by_non_null(df: pl.DataFrame) -> pl.DataFrame:
    # Count non-null values for each column
    non_null_counts = df.select(
        [pl.col(col).drop_nulls().count().alias(col) for col in df.columns]
    )

    # Convert to dictionary and filter columns with non-null values greater than 0
    sorted_columns = dict(
        zip(non_null_counts.columns, non_null_counts.row(0))
    )  # Convert to dictionary
    sorted_columns = {k: v for k, v in sorted_columns.items() if v > 0}

    # Sort columns by non-null counts in descending order
    sorted_columns = sorted(sorted_columns.items(), key=lambda x: x[1], reverse=True)

    # Convert sorted columns back to DataFrame
    sorted_columns_df = pl.DataFrame(
        {
            "column": [col for col, _ in sorted_columns],
            "count": [count for _, count in sorted_columns],
        }
    )

    return sorted_columns_df


def print_results(total_rows, sorted_columns_df, title):
    print(f"Total rows: {total_rows}")
    print(f"{title}:")
    for row in sorted_columns_df.iter_rows(named=True):
        print(f"{row['column']}: {row['count']}")


# Load datasets
df = load_data(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\1- Projects\dim_fuelcard_202409191058.csv"
)

# Count total rows in each DataFrame
total_rows_df = count_total_rows(df)

# Sort columns by the number of non-null values
sorted_columns_df = sort_columns_by_non_null(df)

# Print results
print_results(total_rows_df, sorted_columns_df, "Counts")
print(df.count())

# Save sorted columns to CSV
sorted_columns_df.write_csv("sortedcolumns.csv")
