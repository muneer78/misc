from ebooklib import epub
from datetime import datetime


def create_ebook_from_text(file_path, book_title, author_name):
    # Read content from text file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Initialize the EPUB book
    book = epub.EpubBook()
    book.set_title(book_title)
    book.add_author(author_name)

    # Set the creation date to the current date
    creation_date = datetime.now().strftime("%Y-%m-%d")
    book.add_metadata("DC", "date", creation_date)

    # Create a chapter with the text content
    chapter = epub.EpubHtml(title="Chapter 1", file_name="chap_01.xhtml")
    chapter.content = f"<html><body><pre>{content}</pre></body></html>"
    book.add_item(chapter)

    # Define the order of items in the book
    book.spine = ["nav", chapter]

    # Write the EPUB file
    epub.write_epub(f"{book_title}.epub", book, {})


# Get user inputs
file_path = input("Enter text file path: ")
ebook_title = input("Enter title: ")
author_name = input("Enter author name: ")

# Create the ebook from text file
create_ebook_from_text(file_path, ebook_title, author_name)
