import os
import re

# Specify the directory containing the files
folder_path = '/Users/muneer78/Desktop/test'  # Replace with your folder path


# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the filename contains spaces or multiple dashes
    if ' ' in filename or '--' in filename:
        # Create the new filename: lowercase, replace spaces with dashes
        new_filename = filename.lower().replace(' ', '-')
        
        # Replace multiple dashes with a single dash
        new_filename = re.sub(r'-+', '-', new_filename)
        
        # Remove special characters (keeping only alphanumeric characters, dashes, and underscores)
        new_filename = re.sub(r'[^a-z0-9-_]', '', new_filename)
        
        # Construct full file paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} -> {new_filename}')

print("File renaming completed!")