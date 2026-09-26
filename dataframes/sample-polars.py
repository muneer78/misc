import polars as pl

# Read the dataset from a CSV file
df1 = pl.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\Parameters_20240327.csv"
)

df_sample = df1.sample(n=5000)

df_sample.write_csv("hubtek20240327sample.csv")
