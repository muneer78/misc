# import os
# import re
#
# def clean_markdown_files(directory):
#     # Define the block to remove
#     block_to_remove = '---\ncategories: great-lines\n\n'
#     block_pattern = re.compile(re.escape(block_to_remove), re.MULTILINE | re.DOTALL)
#
#     # Iterate over all files in the given directory
#     for filename in os.listdir(directory):
#         if filename.endswith('.md'):
#             filepath = os.path.join(directory, filename)
#             print(f"Processing file: {filepath}")
#
#             # Read the existing content of the file
#             with open(filepath, 'r', encoding='utf-8') as file:
#                 existing_content = file.read()
#
#             # Remove only the first occurrence of the block
#             new_content = block_pattern.sub('', existing_content, count=1)
#
#             # Write the modified content back to the file
#             with open(filepath, 'w', encoding='utf-8') as file:
#                 file.write(new_content)
#
#             print(f"Updated file: {filepath}")
# if __name__ == "__main__":
#     directory = '/Users/muneer78/Desktop/saved/'  # Set the directory path here
#     clean_markdown_files(directory)

# import os
#
# # Define the directory containing the files
# directory = '/Users/muneer78/Desktop/saved/'
#
# # Get a list of all files in the directory
# files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
#
# # Function to read file content with a fallback for encoding errors
# def read_file_content(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             return file.readlines()
#     except UnicodeDecodeError:
#         with open(file_path, 'r', encoding='latin-1') as file:
#             return file.readlines()
#
# # Iterate over each file and update its content
# for filename in files:
#     print(f"Processing file: {filename}")
#
#     # Construct full file path
#     file_path = os.path.join(directory, filename)
#
#     # Extract title from the filename
#     if 'great-lines-' in filename:
#         file_base, file_ext = os.path.splitext(filename)
#         title_parts = file_base.split('great-lines-', 1)[1].replace('-', ' ')
#         title = title_parts.title()
#         full_title = f'Great Lines: {title}'
#         print(f"Generated title: {full_title}")
#
#         # Read the content of the file
#         content = read_file_content(file_path)
#
#         # Prepare the new header to add at the top
#         new_header = f"---\ncategories: great-lines\ntitle: \"{full_title}\"\n\n"
#
#         # Remove existing title and category blocks
#         within_front_matter = False
#         cleaned_content = []
#         for line in content:
#             if line.strip() == "---":
#                 within_front_matter = not within_front_matter
#                 continue  # Skip the delimiter lines
#             if within_front_matter:
#                 if line.strip().startswith(("categories:", "title:")):
#                     continue  # Skip any existing categories or title lines
#             if line.strip().startswith("Great Lines:"):
#                 continue  # Skip any duplicate title lines
#             cleaned_content.append(line)
#
#         # Combine the new header with the filtered content
#         final_content = [new_header] + cleaned_content
#
#         # Write the updated content back to the file
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.writelines(final_content)
#
#         print(f"Updated file: {filename}")
#     else:
#         print(f"Skipping file: {filename}, no 'great-lines-' in filename")
#
# print("File processing complete.")

# import os
#
# # Define the directory containing the files
# directory = '/Users/muneer78/Desktop/saved/'
#
# # Get a list of all files in the directory
# files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
#
# # Function to read file content with a fallback for encoding errors
# def read_file_content(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             return file.readlines()
#     except UnicodeDecodeError:
#         with open(file_path, 'r', encoding='latin-1') as file:
#             return file.readlines()
#
# # Iterate over each file and update its content
# for filename in files:
#     print(f"Processing file: {filename}")
#
#     # Construct full file path
#     file_path = os.path.join(directory, filename)
#
#     # Extract title from the filename
#     if 'great-lines-' in filename:
#         file_base, file_ext = os.path.splitext(filename)
#         title_parts = file_base.split('great-lines-', 1)[1].replace('-', ' ')
#         title = title_parts.title()
#         full_title = f'Great Lines: {title}'
#         print(f"Generated title: {full_title}")
#
#         # Read the content of the file
#         content = read_file_content(file_path)
#
#         # Prepare the new header to add at the top
#         new_header = f"---\ncategories: great-lines\ntitle: \"{full_title}\"\n---\n\n"
#
#         # Remove existing title and category blocks
#         within_front_matter = False
#         cleaned_content = []
#         for line in content:
#             if line.strip() == "---":
#                 within_front_matter = not within_front_matter
#                 continue  # Skip the delimiter lines
#             if within_front_matter:
#                 if line.strip().startswith(("categories:", "title:")):
#                     continue  # Skip any existing categories or title lines
#             if line.strip().startswith("Great Lines:"):
#                 continue  # Skip any duplicate title lines
#             cleaned_content.append(line)
#
#         # Combine the new header with the filtered content
#         final_content = [new_header] + cleaned_content
#
#         # Ensure the file ends with '---\n'
#         if not final_content[-1].strip() == "---":
#             final_content.append("---\n")
#
#         # Write the updated content back to the file
#         with open(file_path, 'w', encoding='utf-8') as file:
#             file.writelines(final_content)
#
#         print(f"Updated file: {filename}")
#     else:
#         print(f"Skipping file: {filename}, no 'great-lines-' in filename")
#
# print("File processing complete.")

import os
import re

# Directory where the markdown files are located
directory = "/Users/muneer78/Desktop/saved/"

# Regex to match the added title line
title_line_pattern = re.compile(r'^title: ".+"\n', re.MULTILINE)

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".md"):
        file_path = os.path.join(directory, filename)

        with open(file_path, 'r') as file:
            content = file.read()

        # Remove the added title line
        new_content = title_line_pattern.sub('', content)

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(new_content)
