import csv
from datetime import datetime
from pathlib import Path

# File paths
input_csv = Path(
    "/Users/muneer78/Downloads/Instapaper-Export-2025-04-20_01_15_08.csv"
)  # Replace with your CSV file path
output_md = Path(
    "/Users/muneer78/Downloads/instapaper_links_sorted.md"
)  # Output Markdown file

# Read the CSV file and extract links
links = []
with open(input_csv, "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        url = row[0]
        title = row[1]
        timestamp = row[4]

        # Convert timestamp to readable date
        date = datetime.utcfromtimestamp(int(timestamp)).strftime("%Y-%m-%d")

        # Append the link data
        links.append((date, title, url))

# Sort links by date
links.sort(key=lambda x: x[0])

# Prepare Markdown content
markdown_lines = [
    "---",
    f"date: {datetime.now().strftime('%Y-%m-%d')}",
    f"title: Instapaper links from {datetime.now().strftime('%Y-%m-%d')}",
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
