from bs4 import BeautifulSoup
from pathlib import Path

# File paths
input_html = Path(
    "/Users/muneer78/Downloads/pinboard_export.2025.05.03_14.58.html"
)  # Replace with the path to your HTML file
output_md = Path(
    "/Users/muneer78/Downloads/links.md"
)  # Replace with the desired output Markdown file path

# Read the HTML file
with input_html.open("r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract links and metadata
links = []
for a_tag in soup.find_all("a", href=True):
    title = a_tag.text.strip() if a_tag.text.strip() else "Untitled"
    url = a_tag["href"]
    date = a_tag.get("add_date", "Unknown Date")  # Use ADD_DATE if available
    links.append(f"- {date}: [{title}]({url})")

# Write to the Markdown file
with output_md.open("w", encoding="utf-8") as file:
    file.write("---\n")
    file.write("date: 2025-05-03\n")  # Replace with the desired date
    file.write("title: Reading List\n")
    file.write("tags: links\n")
    file.write("layout: post\n")
    file.write("---\n\n")
    file.write("\n".join(links))

print(f"Markdown file saved to: {output_md}")
