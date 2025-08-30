from pathlib import Path
import shutil

# Define folder paths
source_dir = Path("C:/Users/YourName/Downloads")
dest_dirs = {
    "Documents": Path("C:/Users/YourName/Documents"),
    "Images": Path("C:/Users/YourName/Pictures"),
}

# Map file extensions to their respective folder
file_type_mapping = {
    ".pdf": "Documents",
    ".docx": "Documents",
    ".jpg": "Images",
    ".png": "Images",
}

# Organize files
for file in source_dir.iterdir():
    if file.is_file():
        file_extension = file.suffix
        if file_extension in file_type_mapping:
            folder_name = file_type_mapping[file_extension]
            destination = dest_dirs[folder_name] / file.name
            shutil.move(str(file), str(destination))  # Convert to string for shutil
