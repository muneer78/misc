from pathlib import Path
from datetime import datetime

# File paths
input_file = Path("/Users/muneer78/Downloads/links.md")  # Input Markdown file
output_file = Path("/Users/muneer78/Downloads/links_converted.md")  # Output Markdown file

# Read the Markdown content
with input_file.open("r", encoding="utf-8") as file:
    lines = file.readlines()

# Function to convert epoch to YYYY-MM-DD
def convert_epoch_to_date(line):
    try:
        # Extract the epoch timestamp (assumes it's at the start of the line)
        if line.startswith("- "):
            parts = line.split(": ", 1)
            epoch = int(parts[0][2:])  # Extract the epoch timestamp
            date = datetime.utcfromtimestamp(epoch).strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD
            return f"- {date}: {parts[1]}"  # Replace the epoch with the formatted date
        return line
    except ValueError:
        return line  # Return the line unchanged if it doesn't match the expected format

# Process each line in the file
converted_lines = [convert_epoch_to_date(line) for line in lines]

# Write the converted content to a new file
with output_file.open("w", encoding="utf-8") as file:
    file.writelines(converted_lines)

print(f"Converted Markdown file saved to: {output_file}")