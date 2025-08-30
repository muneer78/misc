import requests
from bs4 import BeautifulSoup
from ebooklib import epub


def extract_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    return text


def create_epub(urls, output_file):
    book = epub.EpubBook()

    for index, url in enumerate(urls):
        text = extract_text(url)

        # Create a new chapter
        chapter = epub.EpubHtml(
            title=f"Chapter {index + 1}", file_name=f"chapter{index + 1}.xhtml"
        )
        chapter.content = f"<h1>Chapter {index + 1}</h1><p>{text}</p>"

        # Add chapter to the book
        book.add_item(chapter)
        book.toc.append(chapter)
        book.spine.append(chapter)

    # Set the book's metadata
    book.set_title("Extracted Text")
    book.set_language("en")

    # Create EPUB file
    epub.write_epub(output_file, book, {})


# Example usage
urls = [
    "https://newsletter.sarahhaider.com/p/is-the-culture-war-lost",
    "https://newsletter.sarahhaider.com/p/the-woke-have-won-and-decisively",
    "https://newsletter.sarahhaider.com/p/liberalism-is-resilient-the-battle",
    "https://newsletter.sarahhaider.com/p/liberalism-is-easy-to-abandon-wokeism",
    "https://newsletter.sarahhaider.com/p/we-can-come-back-from-the-brink",
    "https://newsletter.sarahhaider.com/p/the-deep-slumber-of-a-decided-opinion",
]

output_file = "Haider.epub"
create_epub(urls, output_file)
print(f'EPUB file "{output_file}" created successfully.')
