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


df_main_orig = pd.read_excel("Excel.xlsx", sheet_name="Master File")
df_lookup_orig = pd.read_csv("file.csv")

df_main = remove_whitespace_from_columns(df_main_orig, "column")
df_lookup = remove_whitespace_from_columns(df_newfuel_orig, "column")


result = pd.merge(
    df_main[["Column 1", "Column 2", "Column 3"]],
    df_lookup,
    on="column1",
    how="inner",
)

# Select only the specified columns in the fuel_result DataFrame
selected_columns = ["Column 1", "Column 2", "Column 3"]

final_result = result[selected_columns]

result.to_csv("result.csv", index=False)
