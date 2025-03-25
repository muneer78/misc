from pathlib import Path

def sort_file_lines_by_title(file_path):
    # Read the file
    with file_path.open('r') as file:
        lines = file.readlines()
    
    # Sort the lines by the title (text between the first two pipes)
    sorted_lines = sorted(
        lines,
        key=lambda line: line.split('|')[1].strip().lower()  # Extract the title and sort case-insensitively
    )
    
    # Write the sorted lines back to the file
    with file_path.open('w') as file:
        file.writelines(sorted_lines)

# Directory containing the files
directory = Path('/Users/muneer78/Downloads')

# Process each file in the directory
for file_path in directory.glob('*.md'):  # Adjust extension if necessary
    sort_file_lines_by_title(file_path)
