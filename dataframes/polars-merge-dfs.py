import polars as pl
from datetime import datetime as dt

# Get the current date
current_date = dt.now()

# Read CSV files into Polars DataFrames
df1 = pl.read_csv("cadence_20240503_182156000.csv")
df2 = pl.read_csv("CadenceSalesforceActiveInactiveCriteria.csv")

# Filter df1 to include only records where 'factorsoft_client_number__c' is not null
df1 = df1.filter(pl.col("factorsoft_client_number__c").is_not_null())

# Filter df2 to include only records where 'active' is False
df2 = df2.filter(pl.col("active") == False)

# Merge df1 and df2 based on 'factorsoft_client_number__c' and 'masterclientno'
merged_df = df1.join(
    df2, left_on="factorsoft_client_number__c", right_on="masterclientno", how="inner"
)

# # Merge df1 and df2 based on 'factorsoft_client_number__c' and 'masterclientno' and find unmatched records
# merged_df = df1.join(
#     df2, left_on="factorsoft_client_number__c", right_on="masterclientno", how="inner"
# )


# Drop duplicates
merged_df = merged_df.unique()

ticket_number = "insert Jira number here"
output_filename = f"DS{ticket_number}_{current_date}_output.csv"

# Write merged DataFrame to CSV
merged_df.write_csv(output_filename)

print("Job done")
