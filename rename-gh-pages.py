import os
from datetime import datetime, timedelta

# Define the directory containing the files
directory = "/Users/muneer78/Documents/GitHub/muneer78.github.io/_posts"

# Get a list of all files in the directory
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Get the current date
current_date = datetime.now()

# Iterate over each file and rename it
for index, filename in enumerate(files):
    # Skip directories (just in case)
    if os.path.isdir(os.path.join(directory, filename)):
        continue

    # Calculate the date for this file
    file_date = current_date - timedelta(days=index)

    # Get the date in the desired format
    date_prefix = file_date.strftime("%Y-%m-%d")

    # Split the filename and its extension
    file_base, file_ext = os.path.splitext(filename)

    # Replace spaces with hyphens and convert to lowercase
    new_file_base = file_base.replace(" ", "-").lower()

    # Construct the new filename
    new_filename = f"{date_prefix}-{new_file_base}{file_ext.lower()}"

    # Construct full old and new file paths
    old_file_path = os.path.join(directory, filename)
    new_file_path = os.path.join(directory, new_filename)

    # Rename the file
    os.rename(old_file_path, new_file_path)

print("Files have been renamed successfully.")
