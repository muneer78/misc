import epub_meta
from pathlib import Path

# Directory containing the EPUB files
ebooks_dir = Path("/Users/muneer78/reading/ebooks/")

# Ensure the directory exists
if not ebooks_dir.exists() or not ebooks_dir.is_dir():
    print(f"Error: The directory '{ebooks_dir}' does not exist or is not a directory.")
else:
    # List to store files with missing metadata fields
    files_with_missing_metadata = []

    # Iterate through all EPUB files in the directory
    for file_path in ebooks_dir.glob("*.epub"):
        try:
            # Extract EPUB metadata
            data = epub_meta.get_epub_metadata(
                file_path, read_cover_image=False, read_toc=False
            )

            # Check if 'authors' or 'title' fields are missing or blank
            if not data.get("authors") or not data.get("title"):
                files_with_missing_metadata.append(file_path.name)
        except Exception as e:
            # Handle any errors that occur during metadata extraction
            print(f"Error processing '{file_path}': {e}")

    # Output the list of files with missing metadata
    if files_with_missing_metadata:
        print("Files with missing 'author' or 'title' metadata:")
        for filename in files_with_missing_metadata:
            print(f"- {filename}")
    else:
        print("All EPUB files have valid 'author' and 'title' metadata.")
