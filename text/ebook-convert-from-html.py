from ebooklib import epub
from bs4 import BeautifulSoup
import markdown2


def create_ebook_from_markdown(md_content, book_title, author_name):
    """
    Convert Markdown content to EPUB format.

    Args:
        md_content (str): Markdown content
        book_title (str): Title of the book
        author_name (str): Name of the author
    """
    # Create an EPUB book
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier("id123456")
    book.set_title(book_title)
    book.set_language("en")
    book.add_author(author_name)

    # Create a chapter from the Markdown content
    chapter = epub.EpubHtml(title="Chapter 1", file_name="chap_01.xhtml", lang="en")
    chapter.content = markdown2.markdown(md_content)

    # Add chapter to the book
    book.add_item(chapter)

    # Define Table Of Contents
    book.toc = (epub.Link("chap_01.xhtml", "Chapter 1", "chap_01"),)

    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = "body { font-family: Arial, sans-serif; }"
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )
    book.add_item(nav_css)

    # Basic spine
    book.spine = ["nav", chapter]

    # Write epub file
    output_filename = f"{book_title.replace(' ', '_')}.epub"
    epub.write_epub(output_filename, book, {})
    print(f"Successfully created: {output_filename}")


def create_ebook(html_file, book_title, author_name):
    """
    Convert an HTML file to EPUB format.

    Args:
        html_file (str): Path to the HTML file
        book_title (str): Title of the book
        author_name (str): Name of the author
    """
    # Read the HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Convert HTML to Markdown
    soup = BeautifulSoup(html_content, "html.parser")
    md_content = markdown2.markdown(soup.get_text())

    # Create EPUB from Markdown content
    create_ebook_from_markdown(md_content, book_title, author_name)


def main():
    try:
        html_file = input("Enter path to HTML file: ")
        book_title = input("Enter book title: ")
        author_name = input("Enter author name: ")

        create_ebook(html_file, book_title, author_name)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
