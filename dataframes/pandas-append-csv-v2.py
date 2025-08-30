import pandas as pd
import os


# Function to convert all columns to strings
def convert_to_strings(df):
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df


directory = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\json"

df_list_new = []

with os.scandir(directory) as it:
    for entry in it:
        if entry.name.endswith(".csv") and entry.is_file():
            df = pd.read_csv(entry.path)
            df_list_new.append(convert_to_strings(df))

# Concatenate all DataFrames
appended_df = pd.concat(df_list_new, ignore_index=True)

# Number of records before dropping duplicates
initial_count = len(appended_df)

# Drop duplicates
final_df = appended_df.drop_duplicates()

# Number of records after dropping duplicates
final_count = len(final_df)

# Number of dropped records
dropped_count = initial_count - final_count

df_sorted = final_df.sort_values(by=["Id"], ascending=False)

# Print the results
print(f"Initial number of records: {initial_count}")
print(f"Number of unique records: {final_count}")
print(f"Number of dropped records: {dropped_count}")

# Save the concatenated DataFrame to a new CSV file
identifier = "DS5339"
df_sorted.to_csv(f"{identifier}_all_records.csv", index=False)

print("CSV files have been successfully appended")
