from pathlib import Path

# Path to the file to process
input_file = Path("/Users/muneer78/Downloads/books.md")

# Output files
duplicates_file = Path("/Users/muneer78/Downloads/duplicates.txt")
cleaned_file = Path("/Users/muneer78/Downloads/cleaned_original.txt")

# Function to extract the text between the first two '|' in a line
def extract_between_pipes(line):
    parts = line.split('|')
    return parts[1].strip() if len(parts) > 2 else None

# Read the original file
with input_file.open('r', encoding='utf-8', errors='ignore') as file:
    lines = file.readlines()

# Dictionary to track duplicates
seen = {}
duplicates = []

# Process lines to find duplicates
for line in lines:
    key = extract_between_pipes(line)
    if key:
        if key in seen:
            duplicates.append(line)
        else:
            seen[key] = line

# Write duplicates to the console and the duplicates file
with duplicates_file.open('w', encoding='utf-8') as dup_file:
    for duplicate in duplicates:
        print(duplicate.strip())  # Log to console
        dup_file.write(duplicate)

# Write the cleaned file with duplicates removed
with cleaned_file.open('w', encoding='utf-8') as clean_file:
    for line in lines:
        key = extract_between_pipes(line)
        if key and key in seen:
            clean_file.write(line)
            del seen[key]  # Ensure each unique line is written only once
