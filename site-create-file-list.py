import os
import csv
import re

def has_html_tags(text):
  """Checks if the given text contains HTML tags."""
  return bool(re.search(r'<[^>]+>', text))

def process_directory(directory, output_file):
  """Processes a directory of Markdown files, writing a CSV of files with HTML tags."""
  with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['filename', 'path']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for root, _, files in os.walk(directory):
      for file in files:
        if file.endswith('.md'):
          file_path = os.path.join(root, file)
          with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if has_html_tags(content):
              writer.writerow({'filename': file, 'path': file_path})

if __name__ == '__main__':
  directory_to_scan = '/Users/muneer78/quartz/content/'  # Replace with your directory
  output_csv_file = 'files_with_html.csv'
  process_directory(directory_to_scan, output_csv_file)