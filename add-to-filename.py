from pathlib import Path
import re

def append_string_to_filenames(directory):
    # Define the suffix to be added
    suffix_to_add = "-video-1"
    # Pattern to match filenames without numeric suffix before the extension
    pattern = re.compile(r"^(.*?)(\.\w+)$")  # Captures base filename and extension

    # Convert directory to a Path object
    directory_path = Path(directory)
    
    if not directory_path.is_dir():
        print(f"The path {directory} is not a valid directory.")
        return
    
    # Iterate through files in the directory
    for file in directory_path.iterdir():
        if file.is_file():
            filename = file.name
            match = pattern.match(filename)
            
            if match:
                base_name, extension = match.groups()
                # Skip files that already have a numeric suffix or the desired suffix
                if not re.search(r"-\d+$", base_name) and not base_name.endswith(suffix_to_add):
                    new_filename = f"{base_name}{suffix_to_add}{extension}"
                    new_file = file.with_name(new_filename)
                    file.rename(new_file)
                    print(f"Renamed: {filename} -> {new_filename}")
                else:
                    print(f"Skipped: {filename}")
            else:
                print(f"Pattern did not match: {filename}")

# Specify the directory to process
directory_path = "/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/PB/videos/"
append_string_to_filenames(directory_path)
