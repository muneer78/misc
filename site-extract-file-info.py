import os
import csv
import re

def extract_metadata(file_path):
  """Extracts date, other text, and tags from a filename and file content.

  Args:
    file_path: The path to the file.

  Returns:
    A tuple of (date, other_text, tags).
  """

  file_name = os.path.basename(file_path)
  match = re.match(r"(\d{4}-\d{2}-\d{2})-(.*)\.(md|markdown)", file_name)
  if not match:
    return None, None, None
  date, other_text = match.groups()[:2]
  other_text = other_text.replace("-", " ").title()

  tags = []
  with open(file_path, 'r') as f:
    for line in f:
      if line.startswith("tags:"):
        tags = line.strip().split("tags:")[1].strip().split(',')
        break

  return date, other_text, tags

def create_csv(directory, csv_file):
  """Creates a CSV file with date, other text, path, and tags for each file in the directory.

  Args:
    directory: The path to the directory.
    csv_file: The path to the output CSV file.
  """

  with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['path', 'date', 'other_text', 'tags']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for root, _, files in os.walk(directory):
      for file in files:
        if file.endswith('.md') or file.endswith('.markdown'):
          file_path = os.path.join(root, file)
          relative_path = os.path.relpath(file_path, directory)  # Calculate relative path
          date, other_text, tags = extract_metadata(file_path)
          if date and other_text:
            writer.writerow({"path": relative_path, "date": date, "other_text": other_text, "tags": ', '.join(tags)})
            print(f"Wrote record: {relative_path}, {date}, {other_text}, {tags}")
          else:
            print(f"Skipped file: {relative_path}")

# Example usage:
directory_to_search = '/Users/muneer78/quartz/content/'
output_csv = 'metadata.csv'
create_csv(directory_to_search, output_csv)