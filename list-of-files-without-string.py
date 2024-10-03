import os
import csv

def find_missing_titles(directory):
  """Finds markdown files without a 'title:' and writes them to a CSV.

  Args:
    directory: The directory to search for markdown files.
  """

  missing_titles = []
  for filename in os.listdir(directory):
    if filename.endswith(".md"):
      file_path = os.path.join(directory, filename)
      with open(file_path, 'r') as f:
        content = f.read()
        if "title:" not in content:
          missing_titles.append(filename)

  with open('missing_titles.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Filename'])
    writer.writerows([[file] for file in missing_titles])

# Example usage:
directory_to_search = '/Users/muneer78/quartz/content/'
find_missing_titles(directory_to_search)
