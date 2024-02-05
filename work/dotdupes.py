import pandas as pd

# Read the CSV files
dot_df = pd.read_csv("DOTDupes.csv")
mc_df = pd.read_csv("MCDupes.csv")

# Find duplicates based on the UID column
dot_duplicates = dot_df[dot_df.duplicated(subset="UID", keep=False)]
mc_duplicates = mc_df[mc_df.duplicated(subset="UID", keep=False)]

# Find common duplicates between the two files
common_duplicates = pd.merge(dot_duplicates, mc_duplicates, on="UID")

# Display the common duplicates
print("Common Duplicates:")
print(common_duplicates)
