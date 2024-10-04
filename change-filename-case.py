import os

# Specify the directory you want to rename files in
directory = '/Users/muneer78/Documents/Projects/'

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file has the specified image extensions
    if filename.lower().endswith(('.jpg', '.jpeg', '.gif', '.png')):
        # Build the full path
        old_path = os.path.join(directory, filename)
        # Convert the file name to lowercase
        new_filename = filename.lower()
        new_path = os.path.join(directory, new_filename)
        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")