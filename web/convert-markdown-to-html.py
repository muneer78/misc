import re
import markdown
from pathlib import Path
from readability import Document
from datetime import datetime

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

def convert_markdown_to_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite', 'sane_lists', 'toc'])
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(filepath).stem
    return title, html_content

markdown_file = '/Users/muneer78/Downloads/ice.md'
title, html_content = convert_markdown_to_html(markdown_file)

doc = Document(html_content)
main_html = doc.summary()  # Preserves formatting

output_path = Path('/Users/muneer78/Downloads/ice_readable.html')
article_html = create_article_html(title, main_html, Path(markdown_file).name)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(article_html)

print(f"Readable HTML saved to {output_path}")