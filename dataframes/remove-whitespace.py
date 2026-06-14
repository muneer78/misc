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
