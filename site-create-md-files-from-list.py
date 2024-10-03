import csv
import re

def sanitize_filename(filename):
    # Remove invalid characters for filenames and ensure it doesn't start or end with a hyphen
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
    return sanitized.strip('-')

def create_markdown_file(tag, title, imagename, date, body):
    # Format title for filename
    filename_title = '-'.join(title.lower().split())
    filename_title = sanitize_filename(filename_title)

    # Check if filename_title is empty
    if not filename_title:
        print(f"Skipping file creation: title '{title}' results in an invalid filename.")
        return

    # Create filename with date and formatted title
    filename = f"{date}-{filename_title}.md"

    # Create content with the specified pattern
    content = f"""---
tags: {tag}
title: "{title}"
date: {date}
---

"""
    # Add the body text
    content += f"""{body}

"""

    # Add the image section only if imagename is not blank
    if imagename:
        content += f"""![{imagename}](https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/{imagename})
        """

    # Write content to the markdown file
    with open(filename, 'w') as file:
        file.write(content)

    print(f"Markdown file '{filename}' created successfully.")

# Read CSV and process rows
csv_file_path = '/Users/muneer78/Documents/Projects/muneericaposts.csv'  # Update this path

try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            tag = row['tag']
            title = row['title']
            imagename = row['filename']
            date = row['date']
            body = row.get('body', '')  # Get the 'body' column, default to an empty string if not present
            create_markdown_file(tag, title, imagename, date, body)
except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
except KeyError as e:
    print(f"Error: Missing column in CSV file - {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
