import os
import re

# Function to extract date from the file content
def extract_date(file_content):
    # Regex pattern to find the date in the format YYYY-MM-DD (even with leading/trailing spaces)
    date_pattern = r"\b\d{4}-\d{2}-\d{2}\b"
    
    for line in file_content:
        match = re.search(date_pattern, line)
        if match:
            print(f"Date found: {match.group()}")  # Debug print
            return match.group().strip()  # Return the date if found
    print("No date found in file.")  # Debug print for files with no date
    return None  # Return None if no date is found

# Directory containing the files
directory = "/Users/muneer78/Desktop/test"

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".md"):  # Only process .md files
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            content = file.readlines()

        # Extract the date from the file content
        date = extract_date(content)

        if date:
            # Create the new filename with the date as a prefix
            new_filename = f"{date}-{filename}"
            new_file_path = os.path.join(directory, new_filename)

            # Check if the file already has the date as a prefix
            if not filename.startswith(date):
                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")
            else:
                print(f"File already has date prefix: {filename}")