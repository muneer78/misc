import os
import ebooklib
from ebooklib import epub
import pandas as pd

def extract_metadata(epub_file):
    book = epub.read_epub(epub_file)
    metadata = {}
    metadata['Title'] = book.get_metadata('DC', 'title', default='Unknown')
    metadata['Author'] = book.get_metadata('DC', 'creator', default='Unknown')
    metadata['Language'] = book.get_metadata('DC', 'language', default='Unknown')
    metadata['Publisher'] = book.get_metadata('DC', 'publisher', default='Unknown')
    metadata['Date'] = book.get_metadata('DC', 'date', default='Unknown')
    return metadata

def process_epub_files(directory):
    metadata_list = []
    for file in os.listdir(directory):
        if file.endswith('.epub'):
            epub_file = os.path.join(directory, file)
            metadata = extract_metadata(epub_file)
            metadata_list.append(metadata)
    return metadata_list

if __name__ == '__main__':
    directory_path = 'path/to/epub_directory'
    metadata_list = process_epub_files(directory_path)
    df = pd.DataFrame(metadata_list)

    print(df)