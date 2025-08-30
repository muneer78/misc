import pandas as pd


def load_and_sort_csv(file_name):
    """Loads a CSV file and sorts it by the 'HistoryKey' column."""
    df = pd.read_csv(file_name)
    df_sorted = df.sort_values(by=["HistoryKey"])
    return df_sorted.reset_index(drop=True)


def find_diff_rows_with_source(name_col="Source", **dfs):
    """
    Finds differing rows between multiple DataFrames and identifies their source.
    Returns a combined DataFrame with a column specifying the origin.

    Parameters:
    - name_col: Name of the source column
    - **dfs: DataFrames provided as keyword arguments with identifiers as keys
    """
    # Add a source identifier column to each DataFrame and combine
    for source, df in dfs.items():
        df[name_col] = source
    combined = pd.concat(dfs.values(), ignore_index=True)

    # Sort the combined DataFrame
    combined = combined.sort_values("HistoryKey").reset_index(drop=True)

    return combined


name = "HistoryKey"

# Load and sort data
df1 = load_and_sort_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\debtorhistory-20241121.csv"
)
df2 = load_and_sort_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\HistoryKey.csv")
df3 = load_and_sort_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\DebtorHistory-20241121-1732201848967.csv"
)

# Find differing rows with their source, handling either 3 or 4 files dynamically
df_diff = find_diff_rows_with_source(PG=df1, DBX=df2, CADENCEPRD=df3)
# df_diff = find_diff_rows_with_source(PG=df1, DBX=df2, CADENCEPRD=df3, RS=df4)

# Save differing rows to a CSV file
output_file = f"{name}-diffs.csv"
df_diff.to_csv(output_file, index=False)

print(f"Differences saved to {output_file}")
