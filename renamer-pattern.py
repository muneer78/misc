from pathlib import Path

# Define the directory containing files
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\Pictures\test")

# Define the naming pattern
base_name = "2023-day-at-the-k-"
extension = ".jpg"
start_number = 1

# Ensure the directory exists
if not directory.exists():
    print(f"Directory {directory} does not exist.")
    exit()

# Get a sorted list of files in the directory
files = sorted(directory.iterdir())  # `iterdir()` lists all files and directories

# Loop through files and rename them
for i, file in enumerate(files):
    if file.is_file():  # Skip directories
        new_name = (
            f"{base_name}{start_number + i:03}{extension}"  # Increment and pad numbers
        )
        new_path = directory / new_name
        file.rename(new_path)
        print(f"Renamed: {file.name} -> {new_name}")
