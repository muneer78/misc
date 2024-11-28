import re
from pathlib import Path

def find_max_values(folder_path):
    """Finds the maximum value in files matching the pattern 'abc-123', 'ghf-345', 'xyz-904'

    Args:
        folder_path: The path to the folder to search.

    Returns:
        A dictionary containing the maximum value for each file pattern.
    """

    max_values = {}
    pattern = re.compile(r"^[a-zA-Z]+-\d+\.[^\.]+$")

    for file in Path(folder_path).rglob("*"):
        if pattern.match(file.name):
            with file.open('r', encoding='latin-1') as f:  # Try Latin-1 encoding
                try:
                    max_value = max(map(float, f.readlines()))
                    prefix = file.stem.split('-')[0]
                    max_values[prefix] = max_value
                except UnicodeDecodeError:
                    print(f"Error decoding file {file.name}")

    return max_values

# Example usage:
folder_path = "/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/PB/videos"
result = find_max_values(folder_path)
print(result)