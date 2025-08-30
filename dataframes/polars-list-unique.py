import polars as pl
from rich import print
from datetime import datetime as dt

# Get the current date
current_date = dt.now()

# List of files to process along with their respective key fields
files_list = [
    ("Region_Update_Leads_NoConverted.csv", "id"),
    ("combinedaccounts.csv", "id"),
]


# Define the function to process each file
def process_file(file_path, key_field):
    try:
        # Read the CSV file into a Polars DataFrame
        df = pl.read_csv(file_path)

        # Calculate unique values for the key field
        unique = df[key_field].n_unique()

        # Calculate duplicate counts for the key field
        dupes_count = len(df) - unique

        # Calculate value counts for the key field
        value_counts = df[key_field].value_counts(sort=True)

        # Print results to console
        print(f"File: {file_path}")
        print(f"Number of unique records in file: {unique}")
        print(f"Number of duplicate records in file: {dupes_count}")
        print("Value counts:")
        print(value_counts)
        print("\n" + "-" * 40 + "\n")

        return df
    except Exception as e:
        print(f"An error occurred while processing the file {file_path}: {e}")
        return None


# Initialize an empty DataFrame
result_df = None


# Iterate through each file and its key field in the list
for file, key in files_list:
    df = process_file(file, key)
    if df is not None:
        if result_df is None:
            result_df = df
        else:
            result_df = result_df.concat(df)

if result_df is not None:
    ticket_number = "4596_Leads"
    output_filename = (
        f"DS{ticket_number}_{current_date.strftime('%Y%m%d%H%M%S')}_output.csv"
    )

    # Filter the DataFrame to keep only unique records based on the 'id' column
    unique_df = result_df.unique(subset=["id"])

    # Save the resulting DataFrame to a CSV file
    unique_df.write_csv(output_filename)
    print(f"Output saved to {output_filename}")
else:
    print("No valid dataframes to save.")
