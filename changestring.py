# import os
#
# # Set the directory where the files are located
# directory = '/Users/muneer78/quartz/content/'  # Replace with the actual directory path
#
# # Loop through each file in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".md"):  # Process only markdown files
#         file_path = os.path.join(directory, filename)
#
#         try:
#             # Read the file content with error handling for encoding issues
#             with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
#                 content = file.read()
#
#             # Replace instances of "greatlines" with "great-lines"
#             new_content = content.replace("metafilter", "strange-researches")
#
#             # Write the updated content back to the file
#             with open(file_path, 'w', encoding='utf-8') as file:
#                 file.write(new_content)
#
#             print(f"Updated {filename}")
#
#         except Exception as e:
#             print(f"Failed to update {filename}: {e}")
#
# print("All files have been updated.")

# import os
# import re
#
# # Directory containing the files
# directory = '/Users/muneer78/Desktop/saved/'
#
# # Regular expression to match the specific title line pattern
# # Example: title: Hong Kong , 1989None
# title_pattern = re.compile(r'^(title:\s*)(.*?)(\s*,\s*)(19\d{2})None$', re.MULTILINE)
#
# def process_title_line(match):
#     title_prefix = match.group(1)  # 'title: '
#     title_text = match.group(2).strip()  # 'Hong Kong' or 'Beirut'
#     comma = ','  # ensuring there is only one comma with correct spacing
#     year = match.group(4)  # '1989' or '1960'
#
#     # Reconstruct the title line without the 'None' and with proper spacing around the comma
#     new_line = f'{title_prefix}{title_text}{comma} {year}'
#
#     print(f"Original line: {match.group(0)}")
#     print(f"Modified line: {new_line}")
#     return new_line
#
# # Iterate over files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith('.md'):
#         filepath = os.path.join(directory, filename)
#
#         with open(filepath, 'r') as file:
#             content = file.read()
#
#         # Apply the regex substitution
#         new_content = title_pattern.sub(process_title_line, content)
#
#         # Check if there are changes
#         if new_content != content:
#             with open(filepath, 'w') as file:
#                 file.write(new_content)
#             print(f'Processed {filename}')
#         else:
#             print(f'No changes made to {filename}')

import os

# Directory containing the files
directory = '/Users/muneer78/Desktop/saved/'

# Function to process each file
def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.startswith("tags:"):
                # Strip the leading "tags:" and split by ","
                line_content = line[len("tags:"):].strip()

                # Remove any leading comma and spaces
                if line_content.startswith(','):
                    line_content = line_content.lstrip(',').strip()

                # Ensure "newsletter" is correctly formatted
                if line_content == "newsletter":
                    new_line = f"tags: {line_content}"
                else:
                    if 'newsletter' in line_content:
                        # Remove "newsletter" if present but not the only text
                        parts = line_content.split('newsletter')
                        # Clean up any trailing commas or spaces
                        new_line_content = parts[0].rstrip(',').strip()
                        if new_line_content:
                            new_line_content += ', '
                        new_line_content += 'newsletter'
                        new_line = f"tags: {new_line_content}"
                    else:
                        # Add ", newsletter" if not present
                        if line_content:
                            new_line_content = line_content.rstrip(',').strip()
                            new_line = f"tags: {new_line_content}, newsletter"
                        else:
                            new_line = "tags: newsletter"

                file.write(new_line + '\n')
            else:
                file.write(line)

# Iterate over files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.md'):  # Adjust if needed
        file_path = os.path.join(directory, filename)
        process_file(file_path)