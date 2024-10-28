import os
import re

def remove_pattern_from_filenames(directory, pattern):
    """
    Removes the specified pattern from filenames in the given directory.

    Args:
        directory: The path to the directory.
        pattern: The regular expression pattern to remove.
    """

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Check if the filename matches the pattern
        if re.search(pattern, filename):
            new_filename = re.sub(pattern, '', filename)
            new_filepath = os.path.join(directory, new_filename)

            print(f"Renaming {filepath} to {new_filepath}")
            os.rename(filepath, new_filepath)

# Replace 'your_directory_path' with the actual path to your directory
directory_path = '/Users/muneer78/Downloads/rename'
pattern = r"\d{1}. "  # Matches two digits followed by a space


remove_pattern_from_filenames(directory_path, pattern)