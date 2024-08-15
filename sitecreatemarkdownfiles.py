# import os
# from datetime import datetime, timedelta
#
# def create_markdown_file(category, title, imagename, date):
#     # Format title for filename
#     filename_title = '-'.join(title.lower().split())
#
#     # Create filename with date and formatted title
#     filename = f"{date.strftime('%Y-%m-%d')}-{filename_title}.md"
#
#     # Create content with the specified pattern
#     content = f"""---
# categories: {category}
# title: {title}
# ---
#
# ![{imagename}](https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/{imagename})
# """
#
#     # Write content to the markdown file
#     with open(filename, 'w') as file:
#         file.write(content)
#
#     print(f"Markdown file '{filename}' created successfully.")
#
# # Example usage
# tuples = [
#     ("funny", "2 Chainz", "2chainz.png"),
#     ("funny", "Ride Or Die", "3am.jpg"),
# ]
#
# # Start date
# start_date = datetime(2023, 1, 8)
#
# for i, (category, title, imagename) in enumerate(tuples):
#     current_date = start_date + timedelta(days=i)
#     create_markdown_file(category, title, imagename, current_date)

'''
Use this section for multiple files
'''

import csv
import re

def sanitize_filename(filename):
    # Remove invalid characters for filenames and ensure it doesn't start or end with a hyphen
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
    return sanitized.strip('-')

def create_markdown_file(category, title, imagename, date):
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
categories: {category}
title: "{title}"
---

![{imagename}](https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/{imagename})
"""

    # Write content to the markdown file
    with open(filename, 'w') as file:
        file.write(content)

    print(f"Markdown file '{filename}' created successfully.")

# Read CSV and process rows
csv_file_path = '/Users/muneer78/Downloads/muneericaposts.csv'  # Update this path

try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            category = row['category']
            title = row['title']
            imagename = row['filename']
            date = row['date']
            create_markdown_file(category, title, imagename, date)
except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
except KeyError as e:
    print(f"Error: Missing column in CSV file - {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
