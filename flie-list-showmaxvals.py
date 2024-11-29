from pathlib import Path
import re
from collections import defaultdict

# Path to the directory containing your files
directory = Path("/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/PB/videos")

# Dictionary to store max numbers for each prefix
group_max = defaultdict(int)

# Regex to match filenames with the format <prefix>-<number>
filename_pattern = re.compile(r"^(.*?)-(\d+)$")

# Iterate through files in the directory
for file in directory.iterdir():
    if file.is_file():  # Ensure it's a file
        match = filename_pattern.match(file.stem)
        if match:
            prefix, number = match.groups()
            number = int(number)
            # Update max number for the prefix
            group_max[prefix] = max(group_max[prefix], number)

# Print the max number for each group
for prefix, max_number in sorted(group_max.items()):
    print(f"{prefix}: {max_number}")
