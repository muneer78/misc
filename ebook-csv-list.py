'''
csv format is as follows
URL,Title
http://example.com/article1,Chapter 1 Title
http://example.com/article2,Chapter 2 Title
'''

import requests
from bs4 import BeautifulSoup
from ebooklib import epub
from datetime import datetime
import csv
import re

def sanitize_filename(name):
    """Remove or replace characters not allowed in filenames."""
    return re.sub(r'[<>:"/\\|?*]', '', name)

def clean_html(content):
    """Clean and sanitize the HTML content."""
    soup = BeautifulSoup(content, 'html.parser')

    # Remove unnecessary tags like scripts and styles
    for tag in soup(['script', 'style']):
        tag.decompose()

    # Extract meaningful content (e.g., article body)
    main_content = soup.find('main') or soup.find('article') or soup.body
    return main_content.prettify() if main_content else soup.prettify()

def create_ebook_with_chapters(csv_file_path, book_title, author_name):
    try:
        # Initialize the EPUB book
        book = epub.EpubBook()
        book.set_title(book_title)

        # Set the author and creation date metadata
        book.add_author(author_name)
        creation_date = datetime.now().strftime('%Y-%m-%d')
        book.add_metadata('DC', 'date', creation_date)

        # Read the CSV and add chapters
        chapters = []
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for index, row in enumerate(reader, start=1):
                url = row.get('URL')
                chapter_title = row.get('Title')
                if not url or not chapter_title:
                    print(f"Skipping row with missing data: {row}")
                    continue

                try:
                    # Fetch content from the URL
                    response = requests.get(url)
                    response.raise_for_status()

                    # Clean and sanitize HTML content
                    html_content = clean_html(response.content)

                    # Sanitize chapter title for filenames
                    sanitized_title = sanitize_filename(chapter_title)

                    # Create a new chapter
                    chapter = epub.EpubHtml(title=chapter_title, file_name=f'chap_{index:02}_{sanitized_title}.xhtml')
                    chapter.content = html_content
                    book.add_item(chapter)
                    chapters.append(chapter)
                    print(f"Added chapter: {chapter_title}")
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching URL {url}: {e}")
                except Exception as e:
                    print(f"Error creating chapter '{chapter_title}': {e}")

        # Add navigation
        book.toc = tuple(chapters)

        # Define the order of items in the book
        book.spine = ['nav'] + chapters

        # Add navigation file
        book.add_item(epub.EpubNav())
        book.add_item(epub.EpubNcx())

        # Write the EPUB file
        epub_file = f"{sanitize_filename(book_title)}.epub"
        epub.write_epub(epub_file, book, {})
        print(f"eBook '{epub_file}' created successfully with {len(chapters)} chapters.")

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except Exception as e:
        print(f"Error creating eBook: {e}")

# Get user inputs
csv_file_path = input('Enter the path to the CSV file: ')
ebook_title = input('Enter the title of the eBook: ')
author_name = input('Enter the author name: ')

# Create the eBook with chapters
create_ebook_with_chapters(csv_file_path, ebook_title, author_name)