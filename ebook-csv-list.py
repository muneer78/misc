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
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Create a new chapter
                    chapter = epub.EpubHtml(title=chapter_title, file_name=f'chap_{index:02}.xhtml')
                    chapter.content = soup.prettify()
                    book.add_item(chapter)
                    chapters.append(chapter)
                    print(f"Added chapter: {chapter_title}")
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching URL {url}: {e}")
                except Exception as e:
                    print(f"Error creating chapter '{chapter_title}': {e}")

        # Define the order of items in the book
        book.spine = ['nav'] + chapters

        # Write the EPUB file
        epub.write_epub(f'{book_title}.epub', book, {})
        print(f"eBook '{book_title}.epub' created successfully with {len(chapters)} chapters.")

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
