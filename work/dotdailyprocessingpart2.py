import pandas as pd
from datetime import date

# Define constant for the filename
FILENAME = "DOTAcctsProcessed.csv"

# Read DOTDupes.csv and DOTAcctsProcessed.csv into pandas dataframes
dot_dupes_df = pd.read_csv("DOTDupes2.csv")
dot_processed_df = pd.read_csv(FILENAME)

# Identify rows that are going to be appended
appended_rows = dot_dupes_df[dot_dupes_df["Processed"].notnull()]

# Append rows from DOTDupes.csv where Processed column is not null to DOTAcctsProcessed.csv
dot_processed_df = dot_processed_df._append(appended_rows, ignore_index=True)

# Convert "DateProcessed" column to datetime type
dot_processed_df["DateProcessed"] = pd.to_datetime(dot_processed_df["DateProcessed"])

# Sort the dataframe by DateProcessed, UID, and dot_number__c
dot_processed_df.sort_values(by=["DateProcessed", "UID", "dot_number__c"], inplace=True)

# Write the updated DOTAcctsProcessed.csv file
dot_processed_df.to_csv(FILENAME, index=False)

# Drop rows where Processed column is not null from DOTDupes.csv
dot_dupes_df = dot_dupes_df[dot_dupes_df["Processed"].isnull()]

# Write the new DOTDupes.csv file
dot_dupes_df.to_csv("DOTDupes.csv", index=False)

dot_reprocess_df = pd.read_csv(FILENAME)

# Update DateProcessed column only for the newly appended rows where DateProcessed is null
dot_reprocess_df["DateProcessed"] = dot_reprocess_df.apply(
    lambda row: pd.to_datetime(str(date.today())).strftime("%m/%d/%Y")
    if pd.isnull(row["DateProcessed"])
    else row["DateProcessed"],
    axis=1,
)

# Write the updated DOTAcctsProcessed.csv file
dot_reprocess_df.to_csv(FILENAME, index=False)

# Filter records with today's date in DateProcessed column
today_records = dot_reprocess_df[
    dot_reprocess_df["DateProcessed"]
    == pd.to_datetime(str(date.today())).strftime("%m/%d/%Y")
]

# Print the number of records with today's date
print("Number of records with today's date:", len(today_records))
