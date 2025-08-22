import csv
from ebooklib import epub
from datetime import datetime
import os
from striprtf.striprtf import rtf_to_text


def create_ebook_from_rtf(file_path, book_title, author_name, output_directory):
    # Read content from RTF file and convert to plain text
    with open(file_path, "r", encoding="utf-8") as file:
        rtf_content = file.read()
        content = rtf_to_text(rtf_content)

    # Initialize the EPUB book
    book = epub.EpubBook()
    book.set_title(book_title)
    book.add_author(author_name)

    # Set the creation date to the current date
    creation_date = datetime.now().strftime("%Y-%m-%d")
    book.add_metadata("DC", "date", creation_date)

    # Create a chapter with the text content
    chapter = epub.EpubHtml(title="Chapter 1", file_name="chap_01.xhtml", lang="en")
    chapter.content = f"<html><body>{''.join(f'<p>{line}</p>' for line in content.splitlines())}</body></html>"
    book.add_item(chapter)

    # Add Table of Contents
    book.toc = (epub.Link("chap_01.xhtml", "Chapter 1", "chap_01"),)

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define the order of items in the book
    book.spine = ["nav", chapter]

    # Define the output path and write the EPUB file
    output_path = os.path.join(output_directory, f"{book_title}.epub")
    epub.write_epub(output_path, book, {})
    print(f"EPUB created at: {output_path}")


# Main function to read CSV and create eBooks
def create_ebooks_from_csv(csv_file_path, output_directory):
    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            file_path = row["file-path"]
            book_title = row["title"]
            author_name = row["author"]
            # Create the eBook
            create_ebook_from_rtf(file_path, book_title, author_name, output_directory)


# Get user inputs for the CSV file path and output directory
csv_file_path = input("Enter CSV file path: ")
output_directory = input("Enter output directory path: ")

# Create eBooks based on CSV entries
create_ebooks_from_csv(csv_file_path, output_directory)
