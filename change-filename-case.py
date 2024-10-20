import os
import re

# Specify the directory you want to rename files in
directory = '/Users/muneer78/EagleFiler/Main/Files/Personal/Pictures'

# Function to add dashes before letters, remove special characters, and replace whitespace with dashes
def add_dashes(name):
    # Replace spaces and underscores with dashes
    name_with_dashes = re.sub(r'[ _]+', '-', name)  # Only replace whitespace and underscores with dashes
    
    # Remove special characters * ' " `
    clean_name = re.sub(r"[*'\"`]", '', name_with_dashes)
    
    return clean_name.lower()  # Convert the entire name to lowercase

# Function to remove extra dashes ("--")
def remove_extra_dash(filename):
    if "--" in filename:
        filename = filename.replace("--", "-", 1)  # Replace first occurrence of "--"
    return filename

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file has the specified image extensions
    if filename.lower().endswith(('.pdf', '.jpg')):
        # Build the full path
        old_path = os.path.join(directory, filename)
        
        # Convert the file name
        name, ext = os.path.splitext(filename)
        new_filename = add_dashes(name) + ext.lower()  # Apply transformations to the filename and convert extension to lowercase
        
        # Remove extra dashes
        new_filename = remove_extra_dash(new_filename)
        
        new_path = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")
