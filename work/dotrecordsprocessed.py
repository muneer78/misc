import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("Duplicate Accounts Workbook.csv")

# Task 1: Take all records where Processed column is not null
processed_df = df[df["Processed"].notnull()]

# Write rows to "DOTAcctsProcessed.csv"
processed_df.to_csv("DOTAcctsProcessed.csv", index=False)

# Task 2: Find all rows where there are duplicate values in "dot_number__c" column
dot_duplicates_df = df[df.duplicated(subset=["dot_number__c"], keep=False)]

# Task 8: Drop records from dot_duplicates_df that are in processed_df
dot_duplicates_df = dot_duplicates_df.merge(
    processed_df[["UID"]], on="UID", how="left", indicator=True
)
dot_duplicates_df = dot_duplicates_df[dot_duplicates_df["_merge"] == "left_only"].drop(
    "_merge", axis=1
)

# Write rows to "DOTDupes.csv"
dot_duplicates_df.to_csv("DOTDupes.csv", index=False)

# Task 3: Find all rows where there are duplicate values in "mc_number__c" column
mc_duplicates_df = df[df.duplicated(subset=["mc_number__c"], keep=False)]

# Task 10: Write records from df not in processed_df, dot_duplicates_df, and mc_duplicates_df to "leftovers.csv"
leftovers_df = df[
    ~df.isin(processed_df) & ~df.isin(dot_duplicates_df) & ~df.isin(mc_duplicates_df)
].dropna()

# Write rows to "leftovers.csv"
leftovers_df.to_csv("leftovers.csv", index=False)

# Task 11: Drop rows from mc_duplicates_df that are in processed_df
mc_duplicates_df = mc_duplicates_df.merge(
    processed_df[["UID"]], on="UID", how="left", indicator=True
)
mc_duplicates_df = mc_duplicates_df[mc_duplicates_df["_merge"] == "left_only"].drop(
    "_merge", axis=1
)

# Exclude records with blank or null values in "mc_number__c" column
mc_duplicates_df = mc_duplicates_df.dropna(subset=["mc_number__c"])

# Sort mc_duplicates_df by mc_number__c column
mc_duplicates_df = mc_duplicates_df.sort_values(by="mc_number__c")

# Write rows to "MCDupes.csv"
mc_duplicates_df.to_csv("MCDupes.csv", index=False)
