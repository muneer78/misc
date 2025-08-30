import polars as pl

# Load the CSV files using Polars
df1 = pl.read_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\algo_filtered.csv")
df2 = pl.read_csv(
    r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\pointdist25-filtered.csv"
)

# Merge the two dataframes on the 'Team' column
merged_df = df1.join(df2, left_on="Team", right_on="TeamName", how="inner")

# Sort the dataframe by the 'final' column in descending order
merged_df_sorted = merged_df.sort("Total", descending=False)
merged_df_sorted = merged_df_sorted.drop("seed")

# Print the sorted dataframe
print(merged_df_sorted.head(10))
print(merged_df_sorted.tail(10))

# Write the sorted dataframe to a CSV file
merged_df_sorted.write_csv(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\merge.csv")
