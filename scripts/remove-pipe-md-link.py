import re
from pathlib import Path

# File paths
input_md = Path("/Users/muneer78/Documents/GitHub/muneer78.github.io/_links/2025-04-19-pocket.md")
output_md = Path("/Users/muneer78/Documents/GitHub/muneer78.github.io/_links/2025-04-19-pocket_cleaned.md")

# Read the Markdown file
with open(input_md, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Process each line to remove text after '|' and before ']'
cleaned_lines = []
for line in lines:
    # Use regex to remove text after '|' and before ']'
    cleaned_line = re.sub(r'\|.*?\]', ']', line)
    cleaned_lines.append(cleaned_line)

# Write the cleaned content to a new Markdown file
with open(output_md, "w", encoding="utf-8") as file:
    file.writelines(cleaned_lines)

print(f"Cleaned Markdown file created: {output_md}")