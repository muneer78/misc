from pathlib import Path

# Define the directory to process
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads")

# Ensure the directory exists
if directory.is_dir():
    for file in directory.iterdir():
        if file.is_file() and file.suffix == ".csv":  # Only process .jpg files
            # Remove the .jpg extension
            new_name = file.stem  # Get the filename without the extension
            new_path = file.with_name(new_name)  # Create the new path

            # Rename the file
            file.rename(new_path)
            print(f"Renamed: {file.name} -> {new_name}")
else:
    print(f"Directory does not exist: {directory}")
