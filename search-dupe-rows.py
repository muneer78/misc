import pandas as pd
from datetime import datetime

# Load your data into a Pandas DataFrame (replace 'data.csv' with your data file)
df1 = pd.read_excel('RTSCS Regional Opportunity  9-8-23.xlsx')
df2 = pd.read_excel('Language Play 9-8-23.xlsx')

def getdupes(df):
    # Find duplicate values in the 'Account Name' column
    duplicates = df[df['Account Name'].duplicated(keep=False)]

    # Create a new DataFrame containing duplicate values
    duplicate_df = duplicates.sort_values(by='Account Name')

    # Optionally, you can reset the index of the new DataFrame
    duplicate_df.reset_index(drop=True, inplace=True)

    return duplicate_df

# Get duplicate dataframes
df1_dupes = getdupes(df1)
df2_dupes = getdupes(df2)

# Get rows where 'Primary Contact: Contact ID' is null
df1_null_contact_id = df1[df1['Primary Contact: Contact ID'].isnull()]
df2_null_contact_id = df2[df2['Primary Contact: Contact ID'].isnull()]

# Get today's date as a string (in the format YYYY-MM-DD)
today_date = datetime.now().strftime('%Y-%m-%d')

# Create an ExcelWriter object with today's date in the filename
output_filename = f'recorderrors_{today_date}.xlsx'
writer = pd.ExcelWriter(output_filename, engine='openpyxl')

# Check if df1_dupes has data before writing it
if not df1_dupes.empty:
    df1_dupes.to_excel(writer, sheet_name='Regional Opp Dupes', index=False)

# Check if df2_dupes has data before writing it
if not df2_dupes.empty:
    df2_dupes.to_excel(writer, sheet_name='Language Play Dupes', index=False)

# Check if df1_null_contact_id has data before writing it
if not df1_null_contact_id.empty:
    df1_null_contact_id.to_excel(writer, sheet_name='Regional Without Contact IDs', index=False)

# Check if df2_null_contact_id has data before writing it
if not df2_null_contact_id.empty:
    df2_null_contact_id.to_excel(writer, sheet_name='Language Without Contact IDs', index=False)

# Close the writer to save the Excel file
writer.close()

print(f'File "{output_filename}" has been saved.')
