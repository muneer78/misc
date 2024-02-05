import pandas as pd

# 1. Read CSV
df = pd.read_csv("BundledFuel.csv")

# 2. Create a dataframe of records meeting the conditions
condition = (df["Bundle Object Status"].isna()) & (
    df["TO DO"].str.contains("SF Team", case=False, na=False)
)
df_filtered = df[condition]

# Write the filtered dataframe to 'filtered_records.csv'
df_filtered.to_csv("bundlefuelfiltered.csv", index=False)

print("All done")
