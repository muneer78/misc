import os
import pandas as pd
import re

# Path to the directory
directory_path = '/Users/muneer78/Desktop/saved'

# Load the updated_file.csv
df = pd.read_csv('updated_file.csv')

# Function to extract date from filename
def extract_date(filename):
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    match = re.search(date_pattern, filename)
    if match:
        return match.group(0)
    return None

# Iterate over each file in the directory
for filename in os.listdir(directory_path):
    # Skip the CSV file itself
    if filename == 'updated_file.csv':
        continue

    # Check if the file name contains any value in the title column
    for index, row in df.iterrows():
        title = row['title']
        postdate = row['postdate']

        if title in filename:
            # Extract the date from the filename
            date = extract_date(filename)

            if date:
                # Replace the date portion of the filename with the date in the postdate column
                new_filename = filename.replace(date, postdate)

                # Get full paths
                old_file = os.path.join(directory_path, filename)
                new_file = os.path.join(directory_path, new_filename)

                # Rename the file
                os.rename(old_file, new_file)
                print(f'Renamed: {filename} to {new_filename}')
