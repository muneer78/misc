from pathlib import Path
import re

# Specify the directory you want to rename files in
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\resources")


# Function to add dashes before letters, remove special characters, and replace whitespace with dashes
def add_dashes(name):
    # Replace spaces and underscores with dashes
    name_with_dashes = re.sub(
        r"[ _]+", "-", name
    )  # Only replace whitespace and underscores with dashes

    # Remove special characters * ' " `
    clean_name = re.sub(r"[*'\"`]", "", name_with_dashes)

    return clean_name.lower()  # Convert the entire name to lowercase


# Function to remove extra dashes ("--")
def remove_extra_dash(filename):
    if "--" in filename:
        filename = filename.replace("--", "-", 1)  # Replace first occurrence of "--"
    return filename


# Loop through all files in the directory
for file in directory.iterdir():
    if file.is_file() and file.suffix.lower() in (
        ".txt",
        ".xlsx",
        ".docx",
        ".md",
        ".py",
        ".sql",
        ".ipynb",
        ".png",
        ".jpg",
        ".gif",
        ".jpeg",
        ".vsdx",
        ".pdf",
        ".html",
        ".csv",
        ".epub",
    ):
        # Convert the file name
        name, ext = file.stem, file.suffix  # Extract name and extension
        new_filename = (
            add_dashes(name) + ext.lower()
        )  # Apply transformations to the filename and convert extension to lowercase

        # Remove extra dashes
        new_filename = remove_extra_dash(new_filename)

        # Define new path and rename
        new_path = file.with_name(new_filename)
        file.rename(new_path)
        print(f"Renamed: {file.name} -> {new_filename}")
