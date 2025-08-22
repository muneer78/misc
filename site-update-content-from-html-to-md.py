import os
import csv
import markdownify

# Directory containing the files to be updated
content_directory = "/Users/muneer78/Desktop/saved/"
# Path to the CSV file
csv_file_path = "files_with_html.csv"


# Function to convert HTML to Markdown
def convert_html_to_markdown(content):
    return markdownify.markdownify(content, heading_style="ATX")


# Function to update file content from HTML to Markdown
def update_file_content(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    print(f"Original content: {content[:500]}")  # Debug: print original content

    markdown_content = convert_html_to_markdown(content)

    print(
        f"Converted content: {markdown_content[:500]}"
    )  # Debug: print converted content

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(markdown_content)


# Read the CSV file
with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
    csv_reader = csv.DictReader(csvfile)

    for row in csv_reader:
        csv_filename = row["filename"]  # Ensure this matches your actual column name
        matched_file = None
        for file in os.listdir(content_directory):
            if file == csv_filename:
                matched_file = os.path.join(content_directory, file)
                print(f"Matched: {matched_file}")  # Debug: print matched file path
                break

        if matched_file:
            update_file_content(matched_file)
            print(f"Updated: {matched_file}")
        else:
            print(f"File not found for: {csv_filename}")
