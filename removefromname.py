import os

# Get the current working directory
current_directory = os.getcwd()

# List all files in the current directory
files = os.listdir(current_directory)

# Iterate through the files and rename them
for file in files:
    if "-hadbomb.com" in file:
        new_name = file.replace("-hadbomb.com", "")
        old_path = os.path.join(current_directory, file)
        new_path = os.path.join(current_directory, new_name)
        os.rename(old_path, new_path)

print(f'Removed "-hadbomb.com" from filenames in {current_directory}')
