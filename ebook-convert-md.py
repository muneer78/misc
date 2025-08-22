import markdown
from ebooklib import epub
from datetime import datetime
import os
from bs4 import BeautifulSoup


def create_ebook(markdown_file, book_title, author_name):
    """
    Convert a Markdown file to EPUB format.

    Args:
        markdown_file (str): Path to the Markdown file
        book_title (str): Title of the book
        author_name (str): Name of the author
    """
    # Check if file exists
    if not os.path.exists(markdown_file):
        raise FileNotFoundError(f"Could not find file: {markdown_file}")

    # Read the Markdown file
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=["extra", "toc"])

    # Create BeautifulSoup object to clean and structure the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Initialize the EPUB book
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier(f"id_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    book.set_title(book_title)
    book.set_language("en")
    book.add_author(author_name)
    creation_date = datetime.now().strftime("%Y-%m-%d")
    book.add_metadata("DC", "date", creation_date)

    # Create chapters based on h1 headers
    chapters = []
    nav_items = []
    current_chapter = None
    chapter_number = 1

    # If no h1 headers found, create a single chapter
    if not soup.find("h1"):
        chapter = epub.EpubHtml(
            title=f"Chapter {chapter_number}",
            file_name=f"chapter_{chapter_number:02d}.xhtml",
        )
        chapter.content = html_content
        chapters.append(chapter)
    else:
        # Split content by h1 headers
        elements = soup.find_all(
            ["h1", "p", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "blockquote"]
        )
        for element in elements:
            if element.name == "h1":
                if current_chapter:
                    chapters.append(current_chapter)

                current_chapter = epub.EpubHtml(
                    title=element.get_text(),
                    file_name=f"chapter_{chapter_number:02d}.xhtml",
                )
                current_chapter.content = f"<h1>{element.get_text()}</h1>"
                chapter_number += 1
            elif current_chapter:
                current_chapter.content += str(element)
            else:
                # Create first chapter if content appears before any h1
                current_chapter = epub.EpubHtml(
                    title="Introduction", file_name="chapter_00.xhtml"
                )
                current_chapter.content = str(element)

        if current_chapter:
            chapters.append(current_chapter)

    # Add chapters to book
    for chapter in chapters:
        book.add_item(chapter)
        nav_items.append(chapter)

    # Create table of contents
    book.toc = [(epub.Section("Table of Contents"), nav_items)]

    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = """
        @namespace epub "http://www.idpf.org/2007/ops";
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 1em; }
        h1 { text-align: center; color: #333; }
        h2 { color: #444; }
        h3 { color: #555; }
    """
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )
    book.add_item(nav_css)

    # Basic spine
    book.spine = ["nav"] + nav_items

    # Write epub file
    output_filename = f"{book_title.replace(' ', '_')}.epub"
    epub.write_epub(output_filename, book, {})
    print(f"Successfully created: {output_filename}")


def main():
    try:
        markdown_file = input("Enter path to Markdown file: ")
        book_title = input("Enter book title: ")
        author_name = input("Enter author name: ")

        create_ebook(markdown_file, book_title, author_name)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
