from pathlib import Path
import re

# Define the pattern you want to match
# match filenames containing string: pattern = re.compile(r'data')
# match filenames starting with string: pattern = re.compile(r'^report')
# match filenames ending with string: pattern = re.compile(r'_2023$')
# Define the pattern you want to match
# pattern = re.compile(r"^business")  # Replace 'your_pattern_here' with your actual pattern

# Replace 'your_pattern_here' with your actual pattern

# Get the current directory
# current_directory = os.getcwd()

# Set directory
directory = Path("/Users/muneer78/Downloads/convert")

# # Loop through the files in the directory
# for file in directory.iterdir():
#     if file.is_file() and pattern.search(file.name) and not file.name.endswith('.pdf'):
#         new_filename = file.name + '.csv'
#         new_path = file.with_name(new_filename)
#         file.rename(new_path)
#         print(f'Renamed: {file.name} to {new_filename}')

for file in directory.iterdir():
    if file.is_file() and not file.name.endswith('.pdf'):
        new_filename = file.name + '.pdf'
        new_path = file.with_name(new_filename)
        file.rename(new_path)
        print(f'Renamed: {file.name} to {new_filename}')