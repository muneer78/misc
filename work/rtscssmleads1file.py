import pandas as pd
from datetime import datetime

# Get today's date as a string (in the format YYYYMMDD)
today_date = datetime.now().strftime("%m-%d-%y")

# Read the Excel files
df = pd.read_excel("RTSCS Regional Opportunity  01-12-24 James Team.xlsx")

# Initialize DataFrames to store removed records
removed_df = pd.DataFrame(columns=df.columns)

# Identify and append rows with blank 'Primary Contact: Contact ID' to the removed rows DataFrames
removed_df = pd.concat([removed_df, df[df["Primary Contact: Contact ID"].isnull()]])

# Remove rows with blank 'Primary Contact: Contact ID' from the original DataFrames
df = df.dropna(subset=["Primary Contact: Contact ID"])

# Identify and append rows with duplicate 'Account Name' values to the removed rows DataFrames
df_duplicates = df[df["Account Name"].duplicated(keep="first")]

removed_df = pd.concat([removed_df, df_duplicates])

# Remove rows with duplicate 'Account Name' values from the original DataFrames
df = df.drop(df_duplicates.index)

# Check if there are any non-null rows left before trying to retrieve one
if not df.dropna().empty:
    first_row_df = df.dropna().iloc[0]
else:
    first_row_df = None

# Fill in specific columns with values from the first non-null row, if available
fill_columns = [
    "Close Date",
    "Campagin ID",
    "Record Type ID",
    "Stage Name",
    "Opportunity Type",
]

if first_row_df is not None:
    for column in fill_columns:
        df[column] = first_row_df[column]

# Extract non-datetime characters from the original filenames and remove spaces and hyphens
file_name = (
    "".join(filter(lambda x: not x.isdigit(), "RTSCS Regional Opportunity"))
    .replace(" ", "")
    .replace("-", "")
)

# Create the output filenames using f-strings
output_filename = f"output_{today_date}_{file_name}.csv"

# Write the DataFrames to CSV files
df.to_csv(output_filename, index=False)

# Create an ExcelWriter object for the removed records only if they are not empty
output_removed_filename = f"removed_records_{today_date}.xlsx"

with pd.ExcelWriter(output_removed_filename, engine="xlsxwriter") as writer:
    if not removed_df.empty:
        removed_df.to_excel(writer, sheet_name="Removed Records", index=False)

print(f'File "{output_filename}" has been saved.')
if not (removed_df.empty):
    print(f'Removed records have been saved to "{output_removed_filename}".')
