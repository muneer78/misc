import requests
from bs4 import BeautifulSoup
from ebooklib import epub


def extract_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    return text


def create_epub(urls, output_file):
    book = epub.EpubBook()

    for index, url in enumerate(urls):
        text = extract_text(url)

        # Create a new chapter
        chapter = epub.EpubHtml(title=f'Chapter {index+1}', file_name=f'chapter{index+1}.xhtml')
        chapter.content = f'<h1>Chapter {index+1}</h1><p>{text}</p>'

        # Add chapter to the book
        book.add_item(chapter)
        book.toc.append(chapter)
        book.spine.append(chapter)

    # Set the book's metadata
    book.set_title('Extracted Text')
    book.set_language('en')

    # Create EPUB file
    epub.write_epub(output_file, book, {})


# Example usage
urls = [
	'https://medium.com/@tomwhitwell/52-things-i-learned-in-2014-91fb546741cc',
   'https://medium.com/magnetic/52-things-i-learned-in-2015-c5c74eed24e0',
   'https://medium.com/magnetic/31-things-fluxx-learned-in-march-2016-b64768bb388',
	'https://medium.com/magnetic/i-spent-two-hours-with-a-mobile-video-genius-and-learned-26-useful-things-1a0b233ce453',
	'https://medium.com/magnetic/52-things-i-learned-in-2016-299fd1e6a62b',
	'https://medium.com/magnetic/52-things-i-learned-in-2017-d9fb0040bdcb',
	'https://medium.com/magnetic/52-things-i-learned-in-2018-b07fc110d8e1',
	'https://medium.com/magnetic/52-things-i-learned-in-2019-8ee483e6c816',
	'https://medium.com/magnetic/52-things-i-learned-in-2020-6a380692dbb8',
	'https://medium.com/magnetic/52-things-i-learned-in-2021-8481c4e0d409',
	'https://medium.com/magnetic/52-things-i-learned-in-2022-db5fcd4aea6e'
]

output_file = 'Things I Learned.epub'
create_epub(urls, output_file)
print(f'EPUB file "{output_file}" created successfully.')