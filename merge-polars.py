import polars as pl


# Read CSV files into Polars DataFrames
df1 = pl.read_csv(r"/Users/muneer78/Downloads/draft-list - merged.csv")
df2 = pl.read_csv(r"/Users/muneer78/Downloads/laghezza-20250314.csv")

# Merge df1 and df2 based on 'factorsoft_client_number__c' and 'masterclientno'
merged_df = df2.join(df1, on="Name", how="left")

# Write merged DataFrame to CSV
merged_df.write_csv("merged.csv")

print("Job done")
