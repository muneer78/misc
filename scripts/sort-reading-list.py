from pathlib import Path
import re

# File paths
input_file = Path("/Users/muneer78/Documents/GitHub/muneer78.github.io/_links/2025-04-18-reading-list.md")
output_file = Path("/Users/muneer78/Documents/GitHub/muneer78.github.io/_links/2025-04-18-reading-list-sorted.md")

# Read the Markdown file
with input_file.open("r", encoding="utf-8") as file:
    lines = file.readlines()

# Extract metadata and links
metadata = []
links = []

for line in lines:
    if line.startswith("- "):  # Identify links
        links.append(line.strip())
    else:  # Keep metadata (YAML front matter or other content)
        metadata.append(line.strip())

# Extract date and sort links by date in descending order
def extract_date(link):
    match = re.match(r"- (\d{4}-\d{2}-\d{2}):", link)
    return match.group(1) if match else "0000-00-00"

sorted_links = sorted(links, key=extract_date, reverse=True)

# Write the sorted content to a new file
with output_file.open("w", encoding="utf-8") as file:
    file.write("\n".join(metadata) + "\n\n")
    file.write("\n".join(sorted_links) + "\n")

print(f"Sorted Markdown file saved to: {output_file}")