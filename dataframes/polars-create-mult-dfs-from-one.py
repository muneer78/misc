import polars as pl


# Function to write dataframe to a file named after the variable name
def write_df_to_csv(df, var_name):
    file_name = f"{var_name}.csv"
    df.write_csv(file_name)
    print(f"Written {var_name} to {file_name}")


# Read CSV
df = pl.read_csv("CadenceSalesforceActiveInactiveCriteria.csv")

# Create a dataframe of records meeting the condition
condition_active = df["active"] == True
df_active = df.filter(condition_active)

condition_inactive = df["active"] == False
df_inactive = df.filter(condition_inactive)

# Write the filtered dataframes to CSV with dynamic names
write_df_to_csv(df_active, "df_active")
write_df_to_csv(df_inactive, "df_inactive")

print("All done")
