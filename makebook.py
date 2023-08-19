from ebooklib import epub

output_filename = "ask a manager-fixed.txt"
epub_filename = "Ask A Manager.epub"

# Read the content from the output file
with open(output_filename, "r") as output_file:
    content = output_file.read()

# Create a new ePub book
book = epub.EpubBook()

# Create a new item (chapter) and add the content
item = epub.EpubHtml(title='Ask A Manager Mistake Stories', file_name='content.xhtml', content=content)
book.add_item(item)

# Define the table of contents
book.toc = (item,)

# Add cover image and metadata (optional)
# book.set_cover("cover.jpg", open("cover.jpg", "rb").read())
book.set_title("Ask A Manager Mistake Stories")
book.set_language("en")

# Create ePub file
epub.write_epub(epub_filename, book, {})

print(f"ePub file '{epub_filename}' created successfully.")