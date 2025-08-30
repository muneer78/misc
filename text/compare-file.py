import os
import difflib

# Directory containing the files
directory = "/Users/muneer78/Documents/GitHub/betlog"

# File extensions to compare
extensions_to_compare = [".py"]  # Add the extensions you want to compare


# Function to compute similarity between two files
def file_similarity(file1, file2):
    # Open files with 'errors="ignore"' to handle non-UTF-8 characters
    with (
        open(file1, "r", encoding="utf-8", errors="ignore") as f1,
        open(file2, "r", encoding="utf-8", errors="ignore") as f2,
    ):
        content1 = f1.readlines()
        content2 = f2.readlines()

    # Use difflib to get a similarity ratio
    diff = difflib.SequenceMatcher(None, content1, content2)
    return diff.ratio()


# Get a list of files in the directory with specific extensions
files = [
    os.path.join(directory, f)
    for f in os.listdir(directory)
    if os.path.isfile(os.path.join(directory, f))
    and os.path.splitext(f)[1] in extensions_to_compare
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

# Sort similar files alphabetically by the first file name
similar_files.sort(key=lambda x: (x[0], x[1]))

# Output similar files
if similar_files:
    print("Files that are 90% or more similar:")
    for file1, file2, sim in similar_files:
        print(f"{file1} and {file2} - Similarity: {sim:.2f}")
else:
    print("No files are 90% or more similar.")
