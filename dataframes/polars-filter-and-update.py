import polars as pl

# Read the dataset from a CSV file
df1 = pl.read_csv("dataset.csv")

df1.filter("shooting > passing")

# Replace 'Somalian' with 'Somali' in the relevant column(s)
df1 = df1.with_columns(
    pl.when(pl.col("LANGUAGE__C") == "Somalian")
    .then("Somali")
    .otherwise(pl.col("LANGUAGE__C"))
    .alias("LANGUAGE__C")
)

# Save the updated DataFrame back to a CSV file
df1 = df1.write_csv("acctreloadupdated.csv")
