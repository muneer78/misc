from pathlib import Path

# Define the two directories
folder1 = Path(r"/Users/muneer78/Documents/Projects/misc/text/")
folder2 = Path(r"/Users/muneer78/Documents/Projects/misc/")

# Iterate through files in folder2
for file2 in folder2.iterdir():
    if file2.is_file():  # Ensure it's a file
        file1 = folder1 / file2.name  # Check for a file with the same name in folder1
        if file1.exists():
            # Compare modification times
            if file2.stat().st_mtime > file1.stat().st_mtime:
                print(f"{file2.name} in folder2 is newer than in folder1")
