import shutil
from pathlib import Path

def copy_and_overwrite(src_file, dest_folder):
    src_path = Path(src_file)
    dest_path = Path(dest_folder) / src_path.name

    # Copy the file and overwrite if it exists
    shutil.copy2(src_path, dest_path)
    print(f"File '{src_path.name}' has been copied to '{dest_folder}' and overwritten if it existed.")

# Example usage
src_file = "/Users/muneer78/scripts/rss-feed-weekly.py"
dest_folder = "/Users/muneer78/Documents/Projects/misc/"

copy_and_overwrite(src_file, dest_folder)