# !/usr/bin/env python3

import sys
import os
import re
from datetime import datetime
from pathlib import Path
import requests
from readability import Document

# Configuration
ARTICLES_DIR = '/Users/muneer78/Documents/GitHub/web-tools/articles/'
INDEX_FILE = '/Users/muneer78/Documents/GitHub/web-tools/article-dir.html'


def create_safe_filename(title):
    """Create a safe filename from article title"""
    safe = re.sub(r'[^a-z0-9]+', '-', title.lower())
    safe = safe.strip('-')[:100]
    timestamp = int(datetime.now().timestamp())
    return f"{safe}-{timestamp}.html"


def fetch_article(url):
    """Fetch and parse article from URL"""
    print(f"Fetching: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    return response.text


def extract_content(html):
    """Extract article content using Readability"""
    print("Extracting article content...")
    doc = Document(html)

    return {
        'title': doc.title(),
        'content': doc.summary()
    }


def create_article_html(article, original_url):
    """Create formatted HTML for the article"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{article['title']}</title>
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
    .meta {{
      color: #666;
      font-size: 0.9em;
      margin-bottom: 2em;
      padding-bottom: 1em;
      border-bottom: 1px solid #ddd;
    }}
    .meta a {{
      color: #0066cc;
    }}
    img {{
      max-width: 100%;
      height: auto;
    }}
  </style>
</head>
<body>
  <h1>{article['title']}</h1>
  <div class="meta">
    <p><strong>Original URL:</strong> <a href="{original_url}">{original_url}</a></p>
    <p><strong>Saved:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  </div>
  <div class="content">
    {article['content']}
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


def save_article(url):
    """Main function to save an article"""
    try:
        # Fetch the page
        html = fetch_article(url)

        # Extract article content
        article = extract_content(html)

        # Create articles directory if needed
        Path(ARTICLES_DIR).mkdir(parents=True, exist_ok=True)

        # Save article
        filename = create_safe_filename(article['title'])
        filepath = os.path.join(ARTICLES_DIR, filename)

        article_html = create_article_html(article, url)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article_html)

        print(f"✓ Saved article to: {filepath}")

        # Update index
        update_index(article['title'], filename)
        print(f"✓ Updated index: {INDEX_FILE}")

        print(f"\n✅ Successfully saved: \"{article['title']}\"")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    # Accept URL from command line or prompt for it
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    else:
        print("Article Archiver")
        print("-" * 40)
        url = input("Enter article URL: ").strip()

        if not url:
            print("❌ No URL provided")
            sys.exit(1)

    save_article(url)