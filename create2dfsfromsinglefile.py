import pandas as pd

# Read CSV
df = pd.read_csv("20230212Competitor.csv")

# Create a dataframe of records meeting the condition
condition = (df["Delete"] = "Y", case=False, na=False)
df_deletes = df[condition]

condition2 = (df["Update"] = "Y", case=False, na=False)
df_updates = df[condition2]

# Write the filtered dataframe to 'filtered_records.csv'
df_deletes.to_csv("competitordelete.csv", index=False)
df_updates.to_csv("competitorupdate.csv", index=False)

print("All done")