import pandas as pd
from datetime import datetime

# Get today's date as a string (in the format YYYYMMDD)
today_date = datetime.now().strftime("%m-%d-%y")

# Read the Excel files
df = pd.read_csv("20t+ Regional Prospecting Opp CSV 10_23_23.csv")

# Initialize DataFrames to store removed records
removed_df = pd.DataFrame(columns=df.columns)

# Identify and append rows with blank 'Contact ID' to the removed rows DataFrames
removed_df = pd.concat([removed_df, df[df["Contact ID"].isnull()]])

# Remove rows with blank 'Primary Contact: Contact ID' from the original DataFrames
df = df.dropna(subset=["Contact ID"])

# Extract non-datetime characters from the original filenames and remove spaces and hyphens
file_name = (
    "".join(filter(lambda x: not x.isdigit(), "RTSF Regional Opportunity"))
    .replace(" ", "")
    .replace("-", "")
)

# Create the output filenames using f-strings
output_filename = f"output_{today_date}_{file_name}.csv"

# Write the DataFrames to CSV files
df.to_csv(output_filename, index=False)

output_removed_filename = f"removed_records_{today_date}.csv"

removed_df.to_csv(output_removed_filename, index=False)

print(f'File "{output_filename}" has been saved.')
if not (removed_df.empty):
    print(f'Removed records have been saved to "{output_removed_filename}".')
