import os

# # Get the current working directory
# current_directory = os.getcwd()
directory = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\test"

# List all files in the current directory
files = os.listdir(directory)

# Iterate through the files and rename them
for file in files:
    if "_" in file:
        new_name = file.replace("_", "-")
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)

print(f'Removed "-" from filenames in {directory}')
