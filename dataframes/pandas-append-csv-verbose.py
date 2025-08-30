import pandas as pd


# Function to convert all columns to strings
def convert_to_strings(df):
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df


# List of CSV files to be appended
csv_files = [
    "Exceptions_20240915.csv",
    "Exceptions_20240309.csv",
    "Exceptions_20240307.csv",
    "Exceptions_20240305.csv",
    "Exceptions_20240707.csv",
    "Exceptions_20240630.csv",
    "Exceptions_20240627.csv",
    "Exceptions_20240908.csv",
    "Exceptions_20240910.csv",
    "Exceptions_20240913.csv",
]

# Read all CSV files and convert all values to strings
df_list = [pd.read_csv(file) for file in csv_files]
df_list = [convert_to_strings(df) for df in df_list]

# Concatenate all DataFrames
appended_df = pd.concat(df_list, ignore_index=True)

# Number of records before dropping duplicates
initial_count = len(appended_df)

# Drop duplicates
final_df = appended_df.drop_duplicates()

# Number of records after dropping duplicates
final_count = len(final_df)

# Number of dropped records
dropped_count = initial_count - final_count

df_sorted = final_df.sort_values(by=["_id"], ascending=False)

# Print the results
print(f"Initial number of records: {initial_count}")
print(f"Number of unique records: {final_count}")
print(f"Number of dropped records: {dropped_count}")

# Save the concatenated DataFrame to a new CSV file
identifier = "DS5088"
df_sorted.to_csv(f"{identifier}_all_records.csv", index=False)

print("CSV files have been successfully appended")
