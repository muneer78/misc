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
#     # Construct full file path
#     file_path = os.path.join(directory, filename)
#
#     # Extract title from the filename
#     file_base, file_ext = os.path.splitext(filename)
#     # Split the filename by hyphens and ignore the date part
#     title_parts = file_base.split('-')[1:]
#     # Capitalize each part of the title and join them with spaces
#     title = ' '.join(word.capitalize() for word in title_parts)
#
#     # Read the content of the file
#     content = read_file_content(file_path)
#
#     # Update the "categories: great lines" line and insert the new title line
#     updated_content = []
#     for line in content:
#         if "categories: great lines" in line:
#             line = "categories: great-lines\n"
#             updated_content.append(line)
#             updated_content.append(f'title: "{title}"\n')
#         else:
#             updated_content.append(line)
#
#     # Write the updated content back to the file
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.writelines(updated_content)
#
# print("Files have been updated successfully.")

# import os
# import re
#
# def update_file_content(directory):
#     for filename in os.listdir(directory):
#         filepath = os.path.join(directory, filename)
#         if os.path.isfile(filepath):
#             with open(filepath, 'r') as file:
#                 content = file.read()
#
#             # Perform the replacement
#             updated_content = re.sub(r"\d{2} \d{2} ([A-Za-z\s]+) ([A-Za-z\s]+)", r"\1: \2", content)
#
#             with open(filepath, 'w') as file:
#                 file.write(updated_content)
#
#             print(f"Updated content in: {filename}")
#
# # Specify your directory here
# directory = '/Users/muneer78/Desktop/saved/'
# update_file_content(directory)

import os
import re

def update_file_content(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                content = file.read()

            # Perform the replacement
            updated_content = re.sub(r"(\w+): (\w+)(.*)", r"\1 \2:\3", content)

            with open(filepath, 'w') as file:
                file.write(updated_content)

            print(f"Updated content in: {filename}")
            
# Specify your directory here
directory = '/Users/muneer78/Desktop/saved/'
update_file_content(directory)
