from bs4 import BeautifulSoup
import requests
from pathlib import Path

# File paths
input_file = Path("/Users/muneer78/Downloads/nonames.md")  # Input Markdown file
output_file = Path("/Users/muneer78/Downloads/links_with_titles.md")  # Output Markdown file

# Read the Markdown content
with input_file.open("r", encoding="utf-8") as file:
    lines = file.readlines()

# Function to fetch the page title
def fetch_page_title(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
        return title
    except Exception as e:
        print(f"Error fetching title for {url}: {e}")
        return "No Title"

# Process each line in the file
updated_lines = []
for line in lines:
    if line.startswith("- "):  # Identify links
        try:
            parts = line.split(": ", 1)
            url_part = parts[1].strip()
            url = url_part[url_part.find("(") + 1 : url_part.find(")")]  # Extract URL from Markdown link
            title = fetch_page_title(url)  # Fetch the page title
            updated_line = f"{parts[0]}: [{title}]({url})\n"  # Replace the title in the Markdown link
            updated_lines.append(updated_line)
        except Exception as e:
            print(f"Error processing line: {line.strip()} - {e}")
            updated_lines.append(line)  # Keep the original line if there's an error
    else:
        updated_lines.append(line)  # Keep metadata or non-link lines unchanged

# Write the updated content to a new file
with output_file.open("w", encoding="utf-8") as file:
    file.writelines(updated_lines)

print(f"Updated Markdown file saved to: {output_file}")