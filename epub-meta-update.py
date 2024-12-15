import zipfile
from ebooklib import epub
from pathlib import Path

# Function to check if the EPUB is a valid ZIP file
def is_valid_epub(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.testzip()  # Test if the ZIP file is valid
        return True
    except (zipfile.BadZipFile, Exception) as e:
        print(f"Error: '{file_path}' is not a valid EPUB or ZIP file. {e}")
        return False

# Function to update EPUB metadata
def update_epub_metadata(file_path, new_author=None, new_title=None):
    try:
        # Check if the file is a valid EPUB
        if not is_valid_epub(file_path):
            return

        # Read the EPUB file
        book = epub.read_epub(file_path)

        # Extract current metadata
        current_title = book.get_metadata('DC', 'title')
        current_author = book.get_metadata('DC', 'creator')

        print("Current Metadata:")
        print(f"Title: {current_title[0][0] if current_title else 'Not set'}")
        print(f"Author(s): {current_author[0][0] if current_author else 'Not set'}")

        # Update metadata fields if new values are provided
        if new_title:
            book.add_metadata('DC', 'title', new_title)
        if new_author:
            book.add_metadata('DC', 'creator', new_author)

        # Save the updated EPUB file (overwrite the original)
        epub.write_epub(file_path, book)

        print("\nMetadata updated successfully.")
        print("Updated Metadata:")
        print(f"Title: {new_title if new_title else 'Not updated'}")
        print(f"Author(s): {new_author if new_author else 'Not updated'}")

    except Exception as e:
        print(f"Error processing '{file_path}': {e}")

# Input file path and metadata values
file_path = Path('/Users/muneer78/reading/ebooks/python-interviews.epub')
new_author = "Mike Driscoll"
new_title = "Python Interviews"

# Ensure the file exists
if file_path.exists() and file_path.is_file():
    update_epub_metadata(file_path, new_author, new_title)
else:
    print(f"Error: The file '{file_path}' does not exist or is not a valid file.")
