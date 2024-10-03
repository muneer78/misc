# import os
# import re
#
# # Directory where the files are located
# directory = "/Users/muneer78/quartz/content/"
#
# # Regular expression to match the date pattern at the start of the filename
# # date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-')
# date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-')
#
#
# # Loop through each file in the directory
# for filename in os.listdir(directory):
#     # Check if the filename starts with a date pattern
#     if date_pattern.match(filename):
#         # Remove the date from the filename
#         new_filename = date_pattern.sub('', filename)
#         # Get the full path for the old and new filenames
#         old_file = os.path.join(directory, filename)
#         new_file = os.path.join(directory, new_filename)
#         # Rename the file
#         os.rename(old_file, new_file)
#         print(f'Renamed: {filename} -> {new_filename}')

# import os
# import re
#
# # Directory where the files are located
# directory = "/Users/muneer78/Desktop/saved/"
#
# # Regular expression to match 'githubpages' in the filename
# name_pattern1 = re.compile(r'githubpages')
# name_pattern2 = 'site'
#
# # Loop through each file in the directory
# for filename in os.listdir(directory):
#     # Search for 'githubpages' in the filename
#     if name_pattern1.search(filename):
#         # Replace 'githubpages' with 'site' in the filename
#         new_filename = name_pattern1.sub(name_pattern2, filename)
#         # Get the full path for the old and new filenames
#         old_file = os.path.join(directory, filename)
#         new_file = os.path.join(directory, new_filename)
#         # Rename the file
#         os.rename(old_file, new_file)
#         print(f'Renamed: {filename} -> {new_filename}')


