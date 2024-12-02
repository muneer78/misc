from pathlib import Path
from ebooklib import epub

# Specify the directory containing the EPUB files
directory = Path("/Users/muneer78/Downloads/test")

# Loop through all EPUB files in the directory
for file in directory.glob("*.epub"):
    try:
        # Read the EPUB metadata
        book = epub.read_epub(file)
        # Extract title and author from the metadata
        title = book.get_metadata("DC", "title")[0][0]  # Title is in a nested tuple
        author = book.get_metadata("DC", "creator")[0][0]  # Author is in a nested tuple
        
        # Extract only the last name of the author
        last_name = author.split()[-1].strip()  # Use the last word as the last name
        
        # Clean and format the extracted metadata
        title_cleaned = title.strip().lower().replace(" ", "-")  # Convert to lowercase and replace spaces with dashes
        last_name_cleaned = last_name.lower().replace(" ", "-")  # Replace spaces with dashes if any
        
        # Create the new filename
        new_filename = f"{last_name_cleaned}-{title_cleaned}.epub"
        new_filepath = directory / new_filename
        
        # Rename the file
        file.rename(new_filepath)
        print(f"Renamed: {file.name} -> {new_filename}")
    except Exception as e:
        print(f"Failed to process {file.name}: {e}")