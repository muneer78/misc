from pathlib import Path
import re

# Define the directory to process
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\Pictures\test")

# Ensure the directory exists
if directory.is_dir():
    for file in directory.iterdir():
        if file.is_file():  # Only process files
            # Remove text within brackets (and the brackets themselves)
            new_name = re.sub(r"\[.*?\]", "", file.name)
            new_name = re.sub(
                r"\(.*?\)", "", new_name
            )  # Optionally handle parentheses as well
            new_name = new_name.strip()  # Remove leading/trailing whitespace

            # Rename the file if the name has changed
            if new_name != file.name:
                new_path = file.with_name(new_name)
                file.rename(new_path)
                print(f"Renamed: {file.name} -> {new_name}")
else:
    print(f"Directory does not exist: {directory}")
