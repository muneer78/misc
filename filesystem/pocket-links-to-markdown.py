import csv
from datetime import datetime
from pathlib import Path

# File paths
input_csv = Path(
    "/Users/muneer78/Downloads/pocket/part_000000.csv"
)  # Replace with your CSV file path
output_md = Path(
    "/Users/muneer78/Downloads/pocket_links_sorted.md"
)  # Output Markdown file

# Read the CSV file and extract links
links = []
with open(input_csv, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        title = row["title"]
        url = row["url"]
        time_added = row["time_added"]

        # Convert timestamp to readable date
        date = datetime.utcfromtimestamp(int(time_added)).strftime("%Y-%m-%d")

        # Append the link data
        links.append((date, title, url))

# Sort links by date
links.sort(key=lambda x: x[0])

# Prepare Markdown content
markdown_lines = [
    "---",
    f"date: {datetime.now().strftime('%Y-%m-%d')}",
    f"title: Pocket links from {datetime.now().strftime('%Y-%m-%d')}",
    "tags: links",
    "layout: post",
    "---",
    "",
]

# Add sorted links to Markdown content
for date, title, url in links:
    markdown_lines.append(f"- {date}: [{title}]({url})")

# Write to Markdown file
with open(output_md, "w", encoding="utf-8") as md_file:
    md_file.write("\n".join(markdown_lines))

print(f"Markdown file created: {output_md}")
