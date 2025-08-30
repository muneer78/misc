from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

current_date = datetime.now().strftime("%Y-%m-%d")

# Load the HTML file
with open(r"/Users/muneer78/Downloads/bookmarks.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Find all bookmark links
links = soup.find_all("a")

# Prepare the Markdown content
markdown_lines = [
    f"---",
    f"date: {current_date}",
    f"title: Posts from {current_date}",
    f"tags: links",
    f"layout: post",
    f"---",
    "",

for link in links:
    url = link.get("href")
    title = link.text
    add_date = link.get("add_date")
    
    # Convert ADD_DATE (if available) to a readable date
    if add_date:
        date = datetime.utcfromtimestamp(int(add_date)).strftime("%Y-%m-%d")
    else:
        date = "Unknown Date"
    
    # Format the line for Markdown
    markdown_lines.append(f"- {date}: [{title}]({url})")

# Write to a Markdown file
with open(f"bookmarks_{current_date}.md", "w", encoding="utf-8") as md_file:
    md_file.write("\n".join(markdown_lines))

print("Markdown file 'bookmarks.md' has been created.")

# File paths
input_file = Path("/Users/muneer78/scripts/bookmarks_2025-04-19.md")
output_file = Path(f"/Users/muneer78/scripts/bookmarks_{current_date}.md")

# Read the Markdown content
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Extract metadata and links
metadata = []
links = []

for line in lines:
    if line.startswith("- "):  # Identify links
        links.append(line.strip())
    else:  # Keep metadata (YAML front matter)
        metadata.append(line.strip())

# Sort links by date
sorted_links = sorted(links, key=lambda x: x.split(":")[0][2:])  # Extract date for sorting

# Write the sorted content to a new file
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(metadata) + "\n\n")
    file.write("\n".join(sorted_links) + "\n")

print(f"Sorted Markdown file saved to: {output_file}")