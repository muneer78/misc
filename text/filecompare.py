from pathlib import Path
import difflib

# Directory containing the files
directory = Path("/Users/muneer78/EagleFiler/Main/code/Files")

# File extensions to compare
extensions_to_compare = [".py"]  # Add the extensions you want to compare


# Function to compute similarity between two files
def file_similarity(file1, file2):
    # Open files with 'errors="ignore"' to handle non-UTF-8 characters
    with (
        file1.open("r", encoding="utf-8", errors="ignore") as f1,
        file2.open("r", encoding="utf-8", errors="ignore") as f2,
    ):
        content1 = f1.readlines()
        content2 = f2.readlines()

    # Use difflib to get a similarity ratio
    diff = difflib.SequenceMatcher(None, content1, content2)
    return diff.ratio()


# Get a list of files in the directory with specific extensions
files = [
    file
    for file in directory.iterdir()
    if file.is_file() and file.suffix in extensions_to_compare
]

# Compare each file with every other file
similar_files = []
threshold = 0.90

for i, file1 in enumerate(files):
    for j, file2 in enumerate(files):
        if i < j:  # Avoid redundant comparisons and self-comparisons
            similarity = file_similarity(file1, file2)
            if similarity >= threshold:
                similar_files.append((file1, file2, similarity))

# Sort similar files by similarity in ascending order
similar_files.sort(key=lambda x: x[2])

# Write the output to a Markdown file
output_file = Path("similar_files.md")
with output_file.open("w", encoding="utf-8") as md_file:
    if similar_files:
        md_file.write("# Files with 90% or More Similarity\n\n")
        for file1, file2, sim in similar_files:
            md_file.write(
                f"- **{file1.name}** and **{file2.name}** - Similarity: {sim:.2f}\n"
            )
    else:
        md_file.write("No files are 90% or more similar.\n")

print(f"Results written to {output_file}")
