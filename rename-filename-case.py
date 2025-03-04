from pathlib import Path
import re

# Specify the directory you want to rename files in
directory = Path('/Users/muneer78/Downloads/videos')

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
for file_path in directory.iterdir():
    # Check if the file has the specified image extensions
    if file_path.suffix.lower() in {'.pdf', '.md', '.txt', '.docx', '.jpg', '.jpeg', '.png', '.gif'}:
        # Convert the file name
        name, ext = file_path.stem, file_path.suffix
        new_filename = add_dashes(name) + ext.lower()  # Apply transformations to the filename and convert extension to lowercase
        
        # Remove extra dashes
        new_filename = remove_extra_dash(new_filename)
        
        new_path = file_path.parent / new_filename
        
        # Rename the file
        file_path.rename(new_path)
        print(f"Renamed: {file_path.name} -> {new_filename}")
