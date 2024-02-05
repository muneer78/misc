import pandas as pd

# 1. Read CSV
file_name = "BIR-10010 MC Auth 202309131411.csv"
df = pd.read_csv(file_name)

# 2. Create a dataframe of records where carrier_authority_date is blank
df_noauthdate = df[df["carrier_authority_date"].isna()]

# Write the dataframe to 'noauthdate.csv'
df_noauthdate.to_csv("noauthdate.csv", index=False)

print("All done")