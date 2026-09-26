import polars as pl

# DS4544


def sortvalues(df):
    # Create temporary columns for case-insensitive sorting
    df = df.with_columns(
        [
            pl.col("LanguageInSalesforce")
            .str.to_lowercase()
            .alias("LanguageInSalesforce_lower")
        ]
    )
    # Sort by these temporary columns
    df = df.sort(["LanguageInSalesforce_lower"])
    # Drop the temporary columns after sorting
    df = df.drop(["LanguageInSalesforce_lower"])
    return df


# Read the CSV file into a DataFrame
df = pl.read_csv("SalesforceProposedNationalOriginValues.csv")

stripped_df = df.with_columns(pl.col("Country_of_Origin").str.strip_chars())

stripped_df = sortvalues(stripped_df)

# Write the filtered DataFrame to an Excel file
stripped_df.write_csv("NationalOriginValues.csv")

print("Done")
