import requests
from bs4 import BeautifulSoup
from ebooklib import epub


def create_ebook(url, book_title):
    # Fetch the content from the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove unwanted elements like headers, footers, nav, and other extraneous sections
    for tag in ["header", "footer", "nav", "aside", ".subscribe", ".login", ".sign-up"]:
        for element in soup.select(tag):
            element.decompose()  # Remove the unwanted elements

    # Extract only the main content of the body
    main_content = soup.find("body")
    if main_content:
        formatted_content = str(main_content)  # Preserve HTML formatting as a string
    else:
        formatted_content = "<p>Content not found.</p>"

    # Create an EPUB book
    book = epub.EpubBook()
    book.set_title(book_title)
    book.set_language("en")  # Set language to English (modify as needed)

    # Add a chapter with the formatted content
    chapter = epub.EpubHtml(title="Chapter 1", file_name="chap_01.xhtml")
    chapter.content = formatted_content  # Preserve HTML formatting
    book.add_item(chapter)

    # Define a table of contents and add it to the spine
    book.toc = (epub.Link("chap_01.xhtml", "Chapter 1", "chap_01"),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Set the book spine
    book.spine = ["nav", chapter]

    # Write the EPUB file
    epub.write_epub(f"{book_title}.epub", book, {})


# User input for the ebook URL and title
ebook_url = input("Enter URL: ")
ebook_title = input("Enter title: ")
create_ebook(ebook_url, ebook_title)
