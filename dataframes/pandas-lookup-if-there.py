import pandas as pd


def remove_whitespace_from_columns(df, columns_to_clean=None):
    """
    Remove leading and trailing whitespace from specified columns in a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns_to_clean (list or None): A list of column names to clean.
            If None, all string columns are cleaned.

    Returns:
        pd.DataFrame: The DataFrame with whitespace removed from specified columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if columns_to_clean is None:
        # If columns_to_clean is not specified, clean all string columns
        columns_to_clean = [col for col in df.columns if df[col].dtype == "object"]

    cleaned_df = df.copy()

    for col in columns_to_clean:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].str.strip()

    return cleaned_df


# Read CSV files
df_main = pd.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\_SET_TIMEZONE_TO_CST6_SELECT_client_key_client_id_client_name_ra-20241125.csv"
)
df_lookup = pd.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\dbx.csv")

# Rename columns in df_lookup for consistency
df_lookup.rename(
    columns={"masterkey": "client_key", "include_credit_rating": "client_rating"},
    inplace=True,
)

# Convert 'created_at' to datetime for sorting
df_main["created_at"] = pd.to_datetime(df_main["created_at"], errors="coerce")

# Keep only the most recent record for each client_key
df_main = (
    df_main.sort_values("created_at", ascending=False)
    .groupby("client_key", as_index=False)
    .first()
)

# Merge the two DataFrames with indicator
result = pd.merge(
    df_main,
    df_lookup,
    on=[
        "client_key",
        "client_rating",
        "top_concentration",
        "sales_month_over_month",
        "missing_collateral",
        "aging_past_due",
        "aggregate_details",
    ],  # Merge on both columns
    how="left",  # Left join to retain all rows from df_main
    indicator=True,  # Add an indicator column to show match status
)

# Add a lookup_match column based on the indicator
result["lookup_match"] = result["_merge"] == "both"

# Drop the indicator column and non-df_main fields
result_final = result[df_main.columns.tolist() + ["lookup_match"]].drop_duplicates()

# Save the result to a CSV file
result_final.to_csv("result.csv", index=False)
