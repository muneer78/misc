import os
from ebooklib import epub
import pandas as pd
from zipfile import BadZipFile


def extract_metadata(epub_file):
    book = None
    try:
        book = epub.read_epub(epub_file)
    except BadZipFile:
        print(f"Skipping {epub_file} - Invalid EPUB format.")
        return None

    metadata = {}
    metadata["Title"] = book.get_metadata("DC", "title")
    metadata["Author"] = book.get_metadata("DC", "creator")
    metadata["Language"] = book.get_metadata("DC", "language")
    metadata["Publisher"] = book.get_metadata("DC", "publisher")
    metadata["Date"] = book.get_metadata("DC", "date")
    return metadata


def process_epub_files(directory):
    metadata_list = []
    for file in os.listdir(directory):
        if file.endswith(".epub"):
            epub_file = os.path.join(directory, file)
            metadata = extract_metadata(epub_file)
            if metadata is not None:
                metadata_list.append(metadata)
    return metadata_list


if __name__ == "__main__":
    directory_path = "/Users/muneer78/Downloads"
    metadata_list = process_epub_files(directory_path)
    df = pd.DataFrame(metadata_list)

    print(df)

df.to_csv("humble.csv", index=False)
