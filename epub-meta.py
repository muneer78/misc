import epub_meta
from pathlib import Path
import json

filename = input('Enter filename (without extension): ')

# Construct the file path using Path
file_path = Path(f'/Users/muneer78/reading/ebooks/{filename}.epub')

# Check if the file exists before proceeding
if not file_path.exists():
    print(f"Error: The file '{file_path}' does not exist.")
else:
    # Extract EPUB metadata
    data = epub_meta.get_epub_metadata(file_path, read_cover_image=True, read_toc=True)
    
    # Remove the cover_image_content field if it exists
    if 'cover_image_content' in data:
        del data['cover_image_content']
    
    # Pretty-print JSON data
    formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_data)
