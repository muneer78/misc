import polars as pl

# DS4581

# Read the dataset from a CSV file
df1 = pl.read_csv("acctreload.csv", columns=["ID", "LANGUAGE__C"])
df2 = pl.read_csv("leadreload.csv", columns=["ID", "LANGUAGE__C"])

# Filter rows where LANGUAGE__C is 'Somalian'
filtered_df2 = df2.filter(pl.col("LANGUAGE__C") == "Somalian")


def replace_somalian_with_somali(df):
    return df.with_columns(
        pl.when(pl.col("LANGUAGE__C") == "Somalian")
        .then(pl.lit("Somali"))
        .otherwise(pl.col("LANGUAGE__C"))
        .alias("LANGUAGE__C")
    )


# Apply the function to dataframesw
updated_df1 = replace_somalian_with_somali(df1)
updated_df2 = replace_somalian_with_somali(filtered_df2)

# Dictionary of dataframes with their names
dfs = {"df1": updated_df1, "df2": updated_df2}

# Apply the function to each dataframe in the dictionary and export to CSV
for name, df in dfs.items():
    updated_name = f"{name}_updated"
    print(f"Updated DataFrame Name: {updated_name}")
    df.write_csv(f"{updated_name}.csv")

print("Job well done!")
