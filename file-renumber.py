from pathlib import Path
import re

def renumber_files(directory):
    # Convert directory to a Path object
    dir_path = Path(directory)
    
    # Regex to match files with the same prefix ending in a number
    pattern = re.compile(r'^(.*?)(\d+)(\.\w+)$')
    
    # Group files by prefix and extension
    grouped_files = {}
    for file in dir_path.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                prefix, number, extension = match.groups()
                key = (prefix, extension)
                grouped_files.setdefault(key, []).append(file)
    
    # Renumber each group
    for (prefix, extension), file_list in grouped_files.items():
        # Sort files by the numerical part
        file_list.sort(key=lambda x: int(pattern.match(x.name).group(2)))
        
        # Renumber files starting from 1
        for i, old_file in enumerate(file_list, start=1):
            new_name = f"{prefix}{i}{extension}"
            new_file = dir_path / new_name
            old_file.rename(new_file)
            print(f"Renamed: {old_file.name} -> {new_file.name}")

# Directory to process
directory = "/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/PB/videos/"  # Replace with your directory path
renumber_files(directory)
