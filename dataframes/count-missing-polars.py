import polars as pl
from rich import print

# Load the data
df1 = pl.read_csv("cadence_20240503_182156000.csv")
df2 = pl.read_csv("CadenceSalesforceActiveInactiveCriteria.csv")

# Count of records that are in df1 but not df2. Drop all duplicates.
df1_not_in_df2 = df1.filter(
    ~df1["factorsoft_client_number__c"].is_in(df2["masterclientno"])
).unique()
df1_not_in_df2_count = df1_not_in_df2.height

# Count of records that are in df2 but not df1. Drop all duplicates.
df2_not_in_df1 = df2.filter(
    ~df2["masterclientno"].is_in(df1["factorsoft_client_number__c"])
).unique()
df2_not_in_df1_count = df2_not_in_df1.height

# Print the counts
print(f"Count of records in df1 but not df2: {df1_not_in_df2_count}")
print(f"Count of records in df2 but not df1: {df2_not_in_df1_count}")
