import requests
from readability import Document
from pathlib import Path

def extract_body_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    doc = Document(response.text)
    title = doc.short_title()
    body_html = doc.summary()
    return title, body_html

url = 'https://www.sfgate.com/sf-culture/article/melania-film-review-21338044.php'  # Replace with your target URL
title, body_html = extract_body_text_from_url(url)

output_path = Path('extracted_body.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title></head><body>{body_html}</body></html>')

print(f'Extracted body text saved to {output_path}')