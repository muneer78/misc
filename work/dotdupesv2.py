import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("Phase_2_-_Duplicate__1705324640037.csv")

# Task 2: Find all rows where there are duplicate values in "dot_number__c" column
dot_duplicates_df = df[df.duplicated(subset=["dot_number__c"], keep=False)]

# Write rows to "DOTDupes.csv"
dot_duplicates_df.to_csv("DOTDupes.csv", index=False)

# Task 3: Find all rows where there are duplicate values in "mc_number__c" column
mc_duplicates_df = df[df.duplicated(subset=["mc_number__c"], keep=False)]

# Create a DataFrame to store records before dropping
records_to_drop_df = mc_duplicates_df.copy()

# Task 11: Remove rows from mc_duplicates_df where "UID" is in dot_duplicates_df
mc_duplicates_df = mc_duplicates_df[
    ~mc_duplicates_df["UID"].isin(dot_duplicates_df["UID"])
]

# Refactor: Exclude records with blank or null values in "mc_number__c" column
records_to_drop_df = records_to_drop_df.dropna(subset=["mc_number__c"])

# Refactor: Sort mc_duplicates_df by mc_number__c column
mc_duplicates_df.sort_values(by="mc_number__c", inplace=True)

# Write rows to "MCDupes.csv"
mc_duplicates_df.to_csv("MCDupes.csv", index=False)

# Write rows to "RecordsToDrop.csv"
records_to_drop_df.to_csv("RecordsToDrop.csv", index=False)
