import csv
from ebooklib import epub
from datetime import datetime
from pathlib import Path
from markdown_it import MarkdownIt


def create_single_ebook_from_csv(csv_file_path, output_directory, default_book_title="My Ebook", default_author="Me"):
    """
    Creates a single EPUB ebook from multiple Markdown files listed in a CSV.

    Args:
        csv_file_path (str): The path to the CSV file.
        output_directory (str): The directory where the EPUB will be saved.
        default_book_title (str): The title to use if the CSV has no title.
        default_author (str): The author to use if the CSV has no author.
    """
    csv_file_path = Path(csv_file_path)
    output_directory = Path(output_directory)

    # Initialize the EPUB book
    book = epub.EpubBook()
    book.set_title(default_book_title)
    book.add_author(default_author)

    # Set the creation date to the current date
    creation_date = datetime.now().strftime("%Y-%m-%d")
    book.add_metadata("DC", "date", creation_date)

    # Initialize the Markdown parser
    md = MarkdownIt()

    chapters = []
    toc_links = []
    chapter_count = 0
    first_row_processed = False

    # Read the CSV and process each file as a chapter
    try:
        with csv_file_path.open(mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                file_path = row.get("file-path")
                chapter_title = row.get("title") or f"Chapter {chapter_count + 1}"

                # Use the first row to set the book's title and author
                if not first_row_processed:
                    book_title = row.get("book-title")
                    author_name = row.get("author")
                    if book_title:
                        book.set_title(book_title)
                    if author_name:
                        book.add_author(author_name)
                    first_row_processed = True

                # Skip if file-path is missing
                if not file_path:
                    print(f"Skipping row due to missing file-path: {row}")
                    continue

                chapter_count += 1

                # Read content from Markdown file
                try:
                    md_path = Path(file_path)
                    content = md_path.read_text(encoding="utf-8")
                except FileNotFoundError:
                    print(f"Warning: File not found at '{file_path}'. Skipping.")
                    continue

                # Convert Markdown content to HTML using the new library
                html_content = md.render(content)
                chapter_content = f"<html><body>{html_content}</body></html>"

                # Create a chapter and add it to the book
                file_name = f"chap_{chapter_count:02d}.xhtml"
                chapter = epub.EpubHtml(title=chapter_title, file_name=file_name, lang="en")
                chapter.content = chapter_content
                book.add_item(chapter)

                # Add the chapter to the lists for spine and TOC
                chapters.append(chapter)
                toc_links.append(epub.Link(file_name, chapter_title, chapter.id))

    except FileNotFoundError:
        print(f"Error: The CSV file was not found at '{csv_file_path}'.")
        return

    # Corrected the way the TOC is structured to avoid TypeError
    book.toc = (epub.Section("Table of Contents", toc_links),)

    # Add Navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define the order of items in the book
    book.spine = ["nav"] + chapters

    # Define the output path and write the EPUB file
    output_directory.mkdir(parents=True, exist_ok=True)
    output_path = output_directory / f"{book.title}.epub"
    epub.write_epub(output_path, book, {})
    print(f"EPUB created at: {output_path}")


if __name__ == "__main__":
    # Get user inputs for the CSV file path and output directory
    print("This script will create a single EPUB ebook from a list of Markdown files in a CSV.")
    csv_file_path = input("Enter the path to your CSV file: ")
    output_directory = input("Enter the path to the output directory: ")

    create_single_ebook_from_csv(csv_file_path, output_directory)
