#!/usr/bin/env python3

import sys
import os
import re
from datetime import datetime
from pathlib import Path
import markdown
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Configuration
ARTICLES_DIR = '/Users/muneer78/Documents/GitHub/web-tools/articles/'
INDEX_FILE = '/Users/muneer78/Documents/GitHub/web-tools/article-dir.html'


def create_safe_filename(title, extension='html'):
    """Create a safe filename from title"""
    safe = re.sub(r'[^a-z0-9]+', '-', title.lower())
    safe = safe.strip('-')[:100]
    timestamp = int(datetime.now().timestamp())
    return f"{safe}-{timestamp}.{extension}"


def convert_markdown_to_html(filepath):
    """Convert markdown file to HTML content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])

    # Extract title (first h1 or use filename)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(filepath).stem

    return title, html_content


def convert_epub_to_html(filepath):
    """Convert EPUB file to HTML content"""
    book = epub.read_epub(filepath)

    # Get title
    title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else Path(filepath).stem

    # Extract all text content
    content_parts = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            content_parts.append(str(soup))

    html_content = '\n'.join(content_parts)

    return title, html_content


def convert_txt_to_html(filepath):
    """Convert plain text file to HTML content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use filename as title
    title = Path(filepath).stem

    # Convert plain text to HTML paragraphs
    paragraphs = content.split('\n\n')
    html_content = '\n'.join([f'<p>{p.replace(chr(10), "<br>")}</p>' for p in paragraphs if p.strip()])

    return title, html_content


def create_article_html(title, content, source_file):
    """Create formatted HTML for the article"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      font-family: Georgia, serif;
      line-height: 1.6;
      color: #333;
    }}
    h1 {{
      font-size: 2em;
      margin-bottom: 0.5em;
    }}
    h2 {{
      font-size: 1.5em;
      margin-top: 1.5em;
    }}
    h3 {{
      font-size: 1.2em;
      margin-top: 1.2em;
    }}
    .meta {{
      color: #666;
      font-size: 0.9em;
      margin-bottom: 2em;
      padding-bottom: 1em;
      border-bottom: 1px solid #ddd;
    }}
    code {{
      background: #f4f4f4;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: 'Courier New', monospace;
    }}
    pre {{
      background: #f4f4f4;
      padding: 15px;
      border-radius: 5px;
      overflow-x: auto;
    }}
    pre code {{
      background: none;
      padding: 0;
    }}
    img {{
      max-width: 100%;
      height: auto;
    }}
    blockquote {{
      border-left: 4px solid #ddd;
      margin-left: 0;
      padding-left: 20px;
      color: #666;
    }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <div class="meta">
    <p><strong>Source:</strong> {source_file}</p>
    <p><strong>Converted:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  </div>
  <div class="content">
    {content}
  </div>
</body>
</html>"""


def update_index(title, filename):
    """Update or create the article directory index"""

    # Create default index if it doesn't exist
    if not os.path.exists(INDEX_FILE):
        index_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Article Directory</title>
  <style>
    body {{
      max-width: 900px;
      margin: 0 auto;
      padding: 20px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    h1 {{
      border-bottom: 3px solid #333;
      padding-bottom: 10px;
    }}
    ul {{
      list-style: none;
      padding: 0;
    }}
    li {{
      padding: 12px;
      margin: 8px 0;
      background: #f5f5f5;
      border-radius: 4px;
      transition: background 0.2s;
    }}
    li:hover {{
      background: #e8e8e8;
    }}
    a {{
      color: #0066cc;
      text-decoration: none;
      font-size: 1.1em;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .date {{
      color: #666;
      font-size: 0.9em;
      margin-left: 10px;
    }}
  </style>
</head>
<body>
  <h1>📚 Article Directory</h1>
  <ul id="article-list">
  </ul>
</body>
</html>"""
    else:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index_html = f.read()

    # Add new article entry at the top of the list (most recent first)
    date_str = datetime.now().strftime('%Y-%m-%d')
    article_link = f'    <li><a href="articles/{filename}">{title}</a><span class="date">{date_str}</span></li>\n'

    # Find the ul tag and insert after it
    ul_start = index_html.find('<ul id="article-list">')
    if ul_start != -1:
        insert_pos = index_html.find('\n', ul_start) + 1
        index_html = index_html[:insert_pos] + article_link + index_html[insert_pos:]

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(index_html)


def process_file(filepath):
    """Process a single file and convert it to an article"""
    try:
        ext = Path(filepath).suffix.lower()
        filename = Path(filepath).name

        print(f"Processing: {filename}")

        # Convert based on file type
        if ext == '.md':
            title, content = convert_markdown_to_html(filepath)
        elif ext == '.epub':
            title, content = convert_epub_to_html(filepath)
        elif ext == '.txt':
            title, content = convert_txt_to_html(filepath)
        else:
            print(f"  ⚠️  Skipping unsupported file type: {ext}")
            return False

        # Create articles directory if needed
        Path(ARTICLES_DIR).mkdir(parents=True, exist_ok=True)

        # Save article
        output_filename = create_safe_filename(title)
        output_path = os.path.join(ARTICLES_DIR, output_filename)

        article_html = create_article_html(title, content, filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(article_html)

        # Update index
        update_index(title, output_filename)

        print(f"  ✓ Converted: \"{title}\"")
        return True

    except Exception as e:
        print(f"  ❌ Error processing {filename}: {str(e)}")
        return False


def process_directory(directory):
    """Process all supported files in a directory"""
    supported_extensions = ['.md', '.epub', '.txt']

    # Find all supported files
    files = []
    for ext in supported_extensions:
        files.extend(Path(directory).glob(f'*{ext}'))

    if not files:
        print(f"No supported files found in {directory}")
        print(f"Looking for: {', '.join(supported_extensions)}")
        return

    print(f"Found {len(files)} file(s) to process\n")

    success_count = 0
    for filepath in sorted(files):
        if process_file(filepath):
            success_count += 1
        print()

    print("=" * 50)
    print(f"✅ Successfully converted {success_count}/{len(files)} files")
    print(f"📁 Articles saved to: {ARTICLES_DIR}/")
    print(f"📄 Index updated: {INDEX_FILE}")


if __name__ == '__main__':
    # Accept directory from command line or prompt for it
    if len(sys.argv) >= 2:
        directory = sys.argv[1]
    else:
        print("Batch Article Converter")
        print("Converts .md, .epub, and .txt files to HTML articles")
        print("-" * 50)
        directory = input("Enter directory path (or press Enter for current directory): ").strip()

        if not directory:
            directory = '.'

    if not os.path.isdir(directory):
        print(f"❌ Error: '{directory}' is not a valid directory")
        sys.exit(1)

    process_directory(directory)