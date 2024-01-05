import pandas as pd
from datetime import date

# Define constant for the filename
FILENAME = "DOTAcctsProcessed.csv"

# Read DOTDupes.csv and DOTAcctsProcessed.csv into pandas dataframes
dot_dupes_df = pd.read_csv("DOTDupes.csv")
dot_processed_df = pd.read_csv(FILENAME)

# Identify rows that are going to be appended
appended_rows = dot_dupes_df[dot_dupes_df["Processed"].notnull()]

# Append rows from DOTDupes.csv where Processed column is not null to DOTAcctsProcessed.csv
dot_processed_df = dot_processed_df._append(appended_rows, ignore_index=True)

# Write the updated DOTAcctsProcessed.csv file
dot_processed_df.to_csv(FILENAME, index=False)

# Drop rows where Processed column is not null from DOTDupes.csv
dot_dupes_df = dot_dupes_df[dot_dupes_df["Processed"].isnull()]

# Write the new DOTDupes.csv file
dot_dupes_df.to_csv("DOTDupes.csv", index=False)

dot_reprocess_df = pd.read_csv(FILENAME)

# Update DateProcessed column only for the newly appended rows where DateProcessed is null
dot_reprocess_df.loc[
    dot_reprocess_df["DateProcessed"].isnull(), "DateProcessed"
] = pd.to_datetime(str(date.today()))

# Write the updated DOTAcctsProcessed.csv file
dot_reprocess_df.to_csv(FILENAME, index=False)

# Filter records with today's date in DateProcessed column
today_records = dot_reprocess_df[
    dot_reprocess_df["DateProcessed"] == pd.to_datetime(str(date.today()))
]

# Print the number of records with today's date
print("Number of records with today's date:", len(today_records))
