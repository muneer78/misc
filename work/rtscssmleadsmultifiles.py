import pandas as pd
from datetime import datetime
import glob
import numpy as np

# Get today's date as a string (in the format YYYYMMDD)
today_date = datetime.now().strftime("%m-%d-%y")


def find_file(pattern):
    files = glob.glob("*.xlsx")
    for f in files:
        if pattern in f:
            return f


def load_file(filepath):
    return pd.read_excel(filepath)


regional_file = find_file("Regional")
lang_file = find_file("Language")

df1 = load_file(regional_file)
df2 = load_file(lang_file)

# Initialize DataFrames to store removed records
removed_df1 = pd.DataFrame(columns=df1.columns)
removed_df2 = pd.DataFrame(columns=df2.columns)

# Identify and append rows with blank 'Primary Contact: Contact ID' to the removed rows DataFrames
removed_df1 = pd.concat([removed_df1, df1[df1["Primary Contact: Contact ID"].isnull()]])
removed_df2 = pd.concat([removed_df2, df2[df2["Primary Contact: Contact ID"].isnull()]])

# Remove rows with blank 'Primary Contact: Contact ID' from the original DataFrames
df1 = df1.dropna(subset=["Primary Contact: Contact ID"])
df2 = df2.dropna(subset=["Primary Contact: Contact ID"])

# Identify and append rows with duplicate 'Account Name' values to the removed rows DataFrames
df1_duplicates = df1[df1["Account Name"].duplicated(keep="first")]
df2_duplicates = df2[df2["Account Name"].duplicated(keep="first")]

removed_df1 = pd.concat([removed_df1, df1_duplicates])
removed_df2 = pd.concat([removed_df2, df2_duplicates])

# Remove rows with duplicate 'Account Name' values from the original DataFrames
df1 = df1.drop(df1_duplicates.index)
df2 = df2.drop(df2_duplicates.index)

# Check if there are any non-null rows left before trying to retrieve one
if not df1.dropna().empty:
    first_row_df1 = df1.dropna().iloc[0]
else:
    first_row_df1 = None

if not df2.dropna().empty:
    first_row_df2 = df2.dropna().iloc[0]
else:
    first_row_df2 = None

# Fill in specific columns with values from the first non-null row, if available
fill_columns = [
    "Close Date",
    "Campagin ID",
    "Record Type ID",
    "Stage Name",
    "Opportunity Type",
]

if first_row_df1 is not None:
    for column in fill_columns:
        df1[column] = first_row_df1[column]

if first_row_df2 is not None:
    for column in fill_columns:
        df2[column] = first_row_df2[column]

# Extract non-datetime characters from the original filenames and remove spaces and hyphens
file1_name = "".join(
    filter(lambda x: not x.isdigit(), "RTSCS Regional Opportunity")
).replace(" ", "")
file2_name = "".join(filter(lambda x: not x.isdigit(), "Language Play")).replace(
    " ", ""
)

removed_df1["RemovalReason"] = np.where(
    removed_df1["Primary Contact: Contact ID"].isnull(),
    "No Contact ID",
    "Duplicate Record",
)
removed_df2["RemovalReason"] = np.where(
    removed_df2["Primary Contact: Contact ID"].isnull(),
    "No Contact ID",
    "Duplicate Record",
)

# Create the output filenames using f-strings
output_filename1 = f"{today_date}_{file1_name}_loadfile.csv"
output_filename2 = f"{today_date}_{file2_name}_loadfile.csv"

# Write the DataFrames to CSV files
df1.to_csv(output_filename1, index=False)
df2.to_csv(output_filename2, index=False)

# Create an ExcelWriter object for the removed records only if they are not empty
output_removed_filename = f"removed_records_{today_date}.xlsx"

with pd.ExcelWriter(output_removed_filename, engine="xlsxwriter") as writer:
    if not removed_df1.empty:
        removed_df1.to_excel(
            writer, sheet_name="Removed Records - Regional", index=False
        )
    if not removed_df2.empty:
        removed_df2.to_excel(
            writer, sheet_name="Removed Records - Language", index=False
        )

print(f'File "{output_filename1}" has been saved.')
print(f'File "{output_filename2}" has been saved.')
if not (removed_df1.empty and removed_df2.empty):
    print(f'Removed records have been saved to "{output_removed_filename}".')
