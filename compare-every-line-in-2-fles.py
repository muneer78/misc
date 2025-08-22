from pathlib import Path

# Paths to the two files
file1_path = Path("/Users/muneer78/Downloads/books.md")
file2_path = Path("/Users/muneer78/Downloads/cleaned_original.md")

# Output files
duplicates_file = Path("/Users/muneer78/Downloads/duplicates.md")
cleaned_file1 = Path("/Users/muneer78/Downloads/cleaned_books.md")
cleaned_file2 = Path("/Users/muneer78/Downloads/cleaned_to_update.md")

# Read the contents of the files
with (
    file1_path.open("r", encoding="utf-8", errors="ignore") as file1,
    file2_path.open("r", encoding="utf-8", errors="ignore") as file2,
):
    lines1 = file1.readlines()
    lines2 = file2.readlines()

# Find duplicates
set1 = set(lines1)
set2 = set(lines2)
duplicates = set1 & set2  # Intersection gives the duplicates

# Write duplicates to a file
with duplicates_file.open("w", encoding="utf-8") as dup_file:
    for line in duplicates:
        dup_file.write(line)

# Write cleaned versions of the original files (removing duplicates)
unique_lines1 = set1 - duplicates
unique_lines2 = set2 - duplicates

with cleaned_file1.open("w", encoding="utf-8") as clean_file1:
    for line in unique_lines1:
        clean_file1.write(line)

with cleaned_file2.open("w", encoding="utf-8") as clean_file2:
    for line in unique_lines2:
        clean_file2.write(line)

print(f"Duplicates written to {duplicates_file}")
print(f"Cleaned versions written to {cleaned_file1} and {cleaned_file2}")
