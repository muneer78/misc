import pandas as pd
import os
import glob


# Function to convert all columns to strings
def convert_to_strings(df):
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df


# Folder containing the CSV files
folder_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads"

# Find all CSV files in the folder where the name begins with 'dev_silver.mongodb'
csv_files = glob.glob(os.path.join(folder_path, "dev_silver.mongodb*.csv"))

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

# Sort the DataFrame by the '_id' column in descending order
df_sorted = final_df.sort_values(by=["_id"], ascending=False)

# Print the results
print(f"Initial number of records: {initial_count}")
print(f"Number of unique records: {final_count}")
print(f"Number of dropped records: {dropped_count}")

# Save the concatenated DataFrame to a new CSV file
identifier = "DS5088"
df_sorted.to_csv(f"{identifier}_all_records.csv", index=False)

print("CSV files have been successfully appended and saved.")
