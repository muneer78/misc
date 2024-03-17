import pandas as pd

# Read CSV
df = pd.read_csv("20230212Competitor.csv")

# Create a dataframe of records meeting the condition
condition_delete = df["Deleted"].str.lower() == "y"
df_deletes = df[condition_delete]

condition_update = df["Update"].str.lower() == "y"
df_updates = df[condition_update]

# Write the filtered dataframe to 'filtered_records.csv'
df_deletes.to_csv("competitordelete.csv", index=False)
df_updates.to_csv("competitorupdate.csv", index=False)

print("All done")
