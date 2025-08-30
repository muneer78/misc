import requests
from bs4 import BeautifulSoup
from ebooklib import epub
from datetime import datetime


def create_ebook(url, book_title, author_name):
    # Fetch the content from the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Initialize the EPUB book
    book = epub.EpubBook()
    book.set_title(book_title)

    # Set the author and creation date metadata
    book.add_author(author_name)
    creation_date = datetime.now().strftime("%Y-%m-%d")
    book.set_metadata("DC", "date", creation_date)

    # Add content to the book
    chapter = epub.EpubHtml(title="Chapter 1", file_name="chap_01.xhtml")
    chapter.content = soup.prettify()
    book.add_item(chapter)

    # Define the order of items in the book
    book.spine = ["nav", chapter]

    # Write the EPUB file
    epub.write_epub(f"{book_title}.epub", book, {})


# Get user inputs
ebook_url = input("Enter URL: ")
ebook_title = input("Enter title: ")
author_name = input("Enter author name: ")

# Create the ebook
create_ebook(ebook_url, ebook_title, author_name)
