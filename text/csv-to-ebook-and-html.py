#!/usr/bin/env python3
"""Turn a CSV of article URLs into a combined HTML file and EPUB.

Install dependencies:
    uv add trafilatura ebooklib beautifulsoup4

Run:
    uv run csv_to_ebook.py articles.csv
    uv run csv_to_ebook.py articles.csv --output weekly-reading --title "Weekly Reading"

The input CSV must contain columns named ``url`` and ``name``.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import trafilatura
from bs4 import BeautifulSoup
from ebooklib import epub


CSS = """
body { font-family: Georgia, serif; line-height: 1.6; margin: 5%; }
main { max-width: 48rem; margin: auto; }
h1, h2, h3, h4 { font-family: Arial, sans-serif; line-height: 1.25; }
article { margin: 3rem 0; }
.source { font: 0.9rem Arial, sans-serif; }
img { max-width: 100%; height: auto; }
""".strip()


@dataclass
class Article:
    name: str
    url: str
    body: str


def slugify(value: str, fallback: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def read_rows(csv_path: Path) -> list[tuple[str, str]]:
    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fields = set(reader.fieldnames or [])
        missing = {"url", "name"} - fields
        if missing:
            raise ValueError(f"Missing CSV column(s): {', '.join(sorted(missing))}")

        rows = []
        for line_number, row in enumerate(reader, start=2):
            name = (row.get("name") or "").strip()
            url = (row.get("url") or "").strip()
            if not name or not url:
                print(f"Skipping row {line_number}: name or URL is blank", file=sys.stderr)
                continue
            rows.append((name, url))
        return rows


def extract_articles(rows: list[tuple[str, str]]) -> list[Article]:
    articles = []
    for position, (name, url) in enumerate(rows, start=1):
        print(f"[{position}/{len(rows)}] Fetching {name}", file=sys.stderr)
        try:
            downloaded = trafilatura.fetch_url(url)
        except Exception as error:  # Network/parser errors should not stop the book.
            print(f"  Failed to download {url}: {error}", file=sys.stderr)
            continue
        if not downloaded:
            print(f"  Failed to download: {url}", file=sys.stderr)
            continue

        body = trafilatura.extract(
            downloaded,
            output_format="html",
            include_links=True,
            include_formatting=True,
            favor_precision=True,
        )
        if not body:
            print(f"  No article body found: {url}", file=sys.stderr)
            continue

        # Trafilatura returns an HTML fragment wrapped in a content container.
        soup = BeautifulSoup(body, "html.parser")
        container = soup.body or soup
        articles.append(Article(name=name, url=url, body=container.decode_contents()))
    return articles


def build_html(articles: list[Article], title: str, output_path: Path) -> None:
    # The numeric prefix keeps anchors unique when names repeat.
    anchors = [
        f"article-{index}-{slugify(article.name, str(index))}"
        for index, article in enumerate(articles, start=1)
    ]
    toc = "\n".join(
        f'<li><a href="#{anchor}">'
        f"{html.escape(article.name)}</a></li>"
        for article, anchor in zip(articles, anchors)
    )
    sections = "\n".join(
        f'''<article id="{anchor}">
<h2>{html.escape(article.name)}</h2>
<p class="source"><a href="{html.escape(article.url, quote=True)}">Original article</a></p>
{article.body}
</article>'''
        for article, anchor in zip(articles, anchors)
    )
    document = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body><main>
<h1>{html.escape(title)}</h1>
<nav aria-label="Table of contents"><h2>Contents</h2><ol>{toc}</ol></nav>
{sections}
</main></body>
</html>
'''
    output_path.write_text(document, encoding="utf-8")


def build_epub(articles: list[Article], title: str, output_path: Path) -> None:
    book = epub.EpubBook()
    book.set_identifier(slugify(title, "collected-articles"))
    book.set_title(title)
    book.set_language("en")

    stylesheet = epub.EpubItem(
        uid="style",
        file_name="style/book.css",
        media_type="text/css",
        content=CSS,
    )
    book.add_item(stylesheet)

    chapters = []
    for index, article in enumerate(articles, start=1):
        chapter = epub.EpubHtml(
            title=article.name,
            file_name=f"chapter-{index:03d}.xhtml",
            lang="en",
        )
        chapter.content = (
            f'<h1>{html.escape(article.name)}</h1>'
            f'<p class="source"><a href="{html.escape(article.url, quote=True)}">'
            f"Original article</a></p>{article.body}"
        )
        chapter.add_item(stylesheet)
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = tuple(chapters)
    book.spine = ["nav", *chapters]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(str(output_path), book)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract article text from a CSV and create HTML and EPUB files."
    )
    parser.add_argument("csv_file", type=Path, help="CSV containing url and name columns")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path without an extension (default: CSV filename)",
    )
    parser.add_argument("--title", default="Collected Articles", help="Book/document title")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_base = args.output or args.csv_file.with_suffix("")

    try:
        rows = read_rows(args.csv_file)
        articles = extract_articles(rows)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if not articles:
        print("Error: no articles were successfully extracted", file=sys.stderr)
        return 1

    output_base.parent.mkdir(parents=True, exist_ok=True)
    html_path = output_base.with_suffix(".html")
    epub_path = output_base.with_suffix(".epub")
    build_html(articles, args.title, html_path)
    build_epub(articles, args.title, epub_path)

    print(f"Created {html_path}")
    print(f"Created {epub_path}")
    print(f"Included {len(articles)} of {len(rows)} CSV rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
