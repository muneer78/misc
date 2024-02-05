import pandas as pd
from datetime import datetime

# Get today's date as a string (in the format YYYYMMDD)
today_date = datetime.now().strftime('%m-%d-%y')

filename1 = f'RTSCS Regional Opportunity {today_date}.csv'
filename2 = f'Language Play {today_date}.csv'

# Read the Excel files
df1 = pd.read_excel(filename1)
df2 = pd.read_excel(filename2)

# Initialize DataFrames to store removed records
removed_df1 = pd.DataFrame(columns=df1.columns)
removed_df2 = pd.DataFrame(columns=df2.columns)

# Identify and append rows with blank 'Primary Contact: Contact ID' to the removed rows DataFrames
removed_df1 = pd.concat([removed_df1, df1[df1['Primary Contact: Contact ID'].isnull()]])
removed_df2 = pd.concat([removed_df2, df2[df2['Primary Contact: Contact ID'].isnull()]])

# Remove rows with blank 'Primary Contact: Contact ID' from the original DataFrames
df1 = df1.dropna(subset=['Primary Contact: Contact ID'])
df2 = df2.dropna(subset=['Primary Contact: Contact ID'])

# Identify and append rows with duplicate 'Account Name' values to the removed rows DataFrames
df1_duplicates = df1[df1['Account Name'].duplicated(keep='first')]
df2_duplicates = df2[df2['Account Name'].duplicated(keep='first')]

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
fill_columns = ['Close Date', 'Campagin ID', 'Record Type ID', 'Stage Name', 'Opportunity Type']

if first_row_df1 is not None:
    for column in fill_columns:
        df1[column] = first_row_df1[column]

if first_row_df2 is not None:
    for column in fill_columns:
        df2[column] = first_row_df2[column]

# Extract non-datetime characters from the original filenames and remove spaces and hyphens
file1_name = ''.join(filter(lambda x: not x.isdigit(), 'RTSCS Regional Opportunity  9-8-23')).replace(' ', '').replace('-', '')
file2_name = ''.join(filter(lambda x: not x.isdigit(), 'Language Play 9-8-23')).replace(' ', '').replace('-', '')

# Create the output filenames using f-strings
output_filename1 = f'output_{today_date}_{file1_name}.csv'
output_filename2 = f'output_{today_date}_{file2_name}.csv'

# Write the DataFrames to CSV files
df1.to_csv(output_filename1, index=False)
df2.to_csv(output_filename2, index=False)

# Create an ExcelWriter object for the removed records only if they are not empty
output_removed_filename = f'removed_records_{today_date}.xlsx'

with pd.ExcelWriter(output_removed_filename, engine='xlsxwriter') as writer:
    if not removed_df1.empty:
        removed_df1.to_excel(writer, sheet_name='Removed Records - File 1', index=False)
    if not removed_df2.empty:
        removed_df2.to_excel(writer, sheet_name='Removed Records - File 2', index=False)

print(f'File "{output_filename1}" has been saved.')
print(f'File "{output_filename2}" has been saved.')
if not (removed_df1.empty and removed_df2.empty):
    print(f'Removed records have been saved to "{output_removed_filename}".')
