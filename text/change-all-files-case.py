import os

# Specify the directory you want to rename files in
directory = "/Users/muneer78/Downloads/convert"

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Build the full path for the old and new filenames
    old_path = os.path.join(directory, filename)
    new_filename = filename.lower()  # Convert the filename to lowercase
    new_path = os.path.join(directory, new_filename)

    # Check if the new path is different and rename the file
    if old_path != new_path:
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")
