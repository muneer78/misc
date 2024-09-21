# import csv
# import os
#
#
# def get_file_name(file_path):
#     """
#     Extracts the filename without extension from a given file path.
#
#     Args:
#         file_path (str): Path to the file.
#
#     Returns:
#         str: Filename without extension.
#     """
#     file_path_components = file_path.split('/')
#     file_name_and_extension = file_path_components[-1].rsplit('.', 1)
#     return file_name_and_extension[0]
#
#
# def add_metadata_to_files(csv_file, directory):
#     """
#     Adds metadata to the top of files in a directory based on information in a CSV.
#
#     Args:
#         csv_file (str): Path to the CSV file containing metadata.
#         directory (str): Path to the directory containing files to modify.
#     """
#
#     print("Reading CSV file...")
#     with open(csv_file, 'r', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         metadata = {}
#         for row in reader:
#             metadata[row['path']] = {
#                 'date': row['date'],
#                 'title': row['title'],
#                 'tags': row['tags']
#             }
#     print("CSV file read successfully.")
#
#     print("Processing files in directory...")
#     for root, _, files in os.walk(directory):
#         for file in files:
#             file_path = os.path.join(root, file)
#             relative_path = os.path.relpath(file_path, directory)
#             file_name = get_file_name(file_path)  # Use the get_file_name function
#             print(f"Checking file: {file_path} ({relative_path})")
#             if relative_path in metadata:
#                 print(f"Processing file: {file_path}")
#                 meta = metadata[relative_path]
#                 with open(file_path, 'r+') as f:
#                     content = f.read()
#                     f.seek(0, 0)
#                     f.write("---\ndate: {}\ntitle: {}\ntags: {}\n---\n{}".format(
#                         meta['date'], meta['title'], meta['tags'], content))
#             else:
#                 print(f"Skipping file: {file_path} (no metadata found)")
#     print("File processing complete.")
#
#
# # Example usage:
# csv_file = 'finalmeta.csv'
# directory = '/Users/muneer78/Desktop/saved/'
# add_metadata_to_files(csv_file, directory)

# import csv
# import os

# def get_file_name(file_path):
#     """
#     Extracts the filename without extension from a given file path.

#     Args:
#         file_path (str): Path to the file.

#     Returns:
#         str: Filename without extension.
#     """
#     file_path_components = file_path.split('/')
#     file_name_and_extension = file_path_components[-1].rsplit('.', 1)
#     return file_name_and_extension[0]

# def remove_front_matter(content):
#     """Removes all occurrences of text between and including '---' delimiters.

#     Args:
#         content: The input text.

#     Returns:
#         The text with all front matter removed.
#     """

#     delimiter = "---"
#     lines = content.splitlines(keepends=True)
#     in_front_matter = False
#     new_lines = []
#     for line in lines:
#         if line.strip() == delimiter:
#             in_front_matter = not in_front_matter
#             continue  # Skip the delimiter line
#         if not in_front_matter:
#             new_lines.append(line)
#     return ''.join(new_lines)

# def add_metadata_to_files(csv_file, directory):
#     """
#     Adds metadata to the top of files in a directory based on information in a CSV,
#     deleting existing front matter if present.

#     Args:
#         csv_file (str): Path to the CSV file containing metadata.
#         directory (str): Path to the directory containing files to modify.
#     """

#     print("Reading CSV file...")
#     with open(csv_file, 'r', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         metadata = {}
#         for row in reader:
#             metadata[row['path']] = {
#                 'date': row['date'],
#                 'title': row['title'],
#                 'tags': row['tags']
#             }
#     print("CSV file read successfully.")

#     print("Processing files in directory...")
#     for root, _, files in os.walk(directory):
#         for file in files:
#             file_path = os.path.join(root, file)
#             relative_path = os.path.relpath(file_path, directory)
#             file_name = get_file_name(file_path)
#             print(f"Checking file: {file_path} ({relative_path})")
#             if relative_path in metadata:
#                 print(f"Processing file: {file_path}")
#                 meta = metadata[relative_path]

#                 with open(file_path, 'r+') as f:
#                     content = f.read()
#                     content = remove_front_matter(content)  # Remove all front matter
#                     f.seek(0)
#                     f.write("---\ndate: {}\ntitle: {}\ntags: {}\n---\n{}".format(
#                         meta['date'], meta['title'], meta['tags'], content))
#             else:
#                 print(f"Skipping file: {file_path} (no metadata found)")
#     print("File processing complete.")


# # Example usage:
# csv_file = 'finalmeta.csv'
# directory = '/Users/muneer78/quartz/content/'
# add_metadata_to_files(csv_file, directory)
