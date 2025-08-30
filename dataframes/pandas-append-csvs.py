import pandas as pd


# Function to convert all columns to strings
def convert_to_strings(df):
    for col in df.columns:
        df[col] = df[col].astype(str)
    return df


# List of CSV files to be appended
csv_files = ["finalerrorfile_1.csv", "finalerrorfile_2.csv", "finalerrorfile_3.csv"]

# Read all CSV files and convert all values to strings
df_list = [pd.read_csv(file) for file in csv_files]
df_list = [convert_to_strings(df) for df in df_list]

# Concatenate all DataFrames
appended_df = pd.concat(df_list, ignore_index=True)

# Save the concatenated DataFrame to a new CSV file
appended_df.to_csv("allerrors.csv", index=False)

print(
    "CSV files have been successfully appended and converted to strings using pandas!"
)
