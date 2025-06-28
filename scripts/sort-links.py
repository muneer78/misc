from pathlib import Path

# File paths
input_file = Path("/Users/muneer78/Documents/GitHub/muneer78.github.io/_links/2025-05-03-reading-list.md")
output_file = Path("/Users/muneer78/Documents/GitHub/muneer78.github.io/_links/2025-05-03-reading-list.md_sorted.md")

# Read the Markdown content
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Separate metadata and links
metadata = []
links = []

for line in lines:
    if line.startswith("- "):  # Identify links
        links.append(line.strip())
    else:  # Keep metadata (YAML front matter)
        metadata.append(line.strip())

# Sort links by date
sorted_links = sorted(links, key=lambda x: x.split(":")[0][2:], reverse=True)  # Extract date for sorting

# Write the sorted content to a new file
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(metadata) + "\n\n")
    file.write("\n".join(sorted_links) + "\n")

print(f"Sorted Markdown file saved to: {output_file}")