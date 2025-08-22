import os
import csv
from bs4 import BeautifulSoup

# Directory containing the files to be updated
content_directory = "/Users/muneer78/Desktop/saved/"
# Path to the CSV file
csv_file_path = "/Users/muneer78/Downloads/html.csv"


# Function to manually convert HTML to GitHub-flavored Markdown
def convert_html_to_gfm(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Example conversions - you can extend this to handle more cases
    for tag in soup.find_all(["b", "strong"]):
        tag.replace_with(f"**{tag.get_text()}**")
    for tag in soup.find_all(["i", "em"]):
        tag.replace_with(f"*{tag.get_text()}*")
    for tag in soup.find_all("a"):
        href = tag.get("href")
        tag.replace_with(f"[{tag.get_text()}]({href})")
    for tag in soup.find_all("img"):
        src = tag.get("src")
        alt = tag.get("alt", "")
        tag.replace_with(f"![{alt}]({src})")

    # Handle other elements as needed

    return soup.get_text()


# Function to update file content, keeping front matter intact
def update_file_content(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Assume front matter is enclosed in "---"
    front_matter = []
    content_start = 0

    if lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                content_start = i + 1
                break
            front_matter.append(line)

    # Convert the rest of the content
    html_content = "".join(lines[content_start:])
    markdown_content = convert_html_to_gfm(html_content)

    # Combine front matter with converted content
    new_content = "---\n" + "".join(front_matter) + "---\n" + markdown_content

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(new_content)


# Read the CSV file
with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
    csv_reader = csv.DictReader(csvfile)

    for row in csv_reader:
        csv_filename = row["filename"]  # Ensure this matches your actual column name
        matched_file = None
        for file in os.listdir(content_directory):
            if file == csv_filename:
                matched_file = os.path.join(content_directory, file)
                print(f"Matched: {matched_file}")
                break

        if matched_file:
            update_file_content(matched_file)
            print(f"Updated: {matched_file}")
        else:
            print(f"File not found for: {csv_filename}")
