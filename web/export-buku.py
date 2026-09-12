#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
buku_export.py — Export buku bookmarks to JSON/Markdown/org/HTML,
excluding one or more tags.

buku stores tags as a comma-delimited string with leading/trailing
commas, e.g. ",work,python,". This script matches on ",tag," to
avoid partial matches (so "py" won't match "python").

Usage:
    uv run buku_export.py --exclude private,scratch --format org -o bookmarks.org
    python3 buku_export.py --exclude private --format json -o bookmarks.json

Defaults:
    --db      ~/.local/share/buku/bookmarks.db
    --format  json
    -o        stdout
"""

import argparse
import html
import json
import sqlite3
import sys
from pathlib import Path


def normalize_tags(raw: str) -> list[str]:
    """buku tag string looks like ',tag1,tag2,' -> ['tag1', 'tag2']"""
    return [t for t in raw.split(",") if t]


def fetch_bookmarks(
    db_path: Path,
    exclude_tags: list[str],
    include_tags: list[str] | None = None,
) -> list[dict]:
    if not db_path.exists():
        sys.exit(f"error: buku DB not found at {db_path}")

    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row

    where_clauses = []
    params = []
    for tag in exclude_tags:
        # exact-tag match via delimiter padding, not substring/fuzzy match
        where_clauses.append("tags NOT LIKE ?")
        params.append(f"%,{tag},%")
    if include_tags:
        include_clauses = []
        for tag in include_tags:
            include_clauses.append("tags LIKE ?")
            params.append(f"%,{tag},%")
        where_clauses.append("(" + " OR ".join(include_clauses) + ")")

    query = "SELECT id, URL, metadata, tags, desc FROM bookmarks"
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " ORDER BY id"

    rows = con.execute(query, params).fetchall()
    con.close()

    return [
        {
            "id": r["id"],
            "url": r["URL"],
            "title": r["metadata"] or "",
            "desc": r["desc"] or "",
            "tags": normalize_tags(r["tags"] or ""),
        }
        for r in rows
    ]


def to_json(bookmarks: list[dict]) -> str:
    return json.dumps(bookmarks, indent=2, ensure_ascii=False)


def to_markdown(bookmarks: list[dict]) -> str:
    lines = ["# Bookmarks", ""]
    for b in bookmarks:
        title = b["title"] or b["url"]
        lines.append(f"- [{title}]({b['url']})")
        if b["tags"]:
            lines.append(f"  - tags: {', '.join(b['tags'])}")
        if b["desc"]:
            lines.append(f"  - {b['desc']}")
    return "\n".join(lines)


def to_org(bookmarks: list[dict]) -> str:
    lines = ["#+TITLE: Bookmarks", ""]
    for b in bookmarks:
        title = b["title"] or b["url"]
        lines.append(f"* [[{b['url']}][{title}]]")
        if b["tags"]:
            tagstr = ":" + ":".join(b["tags"]) + ":"
            lines[-1] += f"  {tagstr}"
        if b["desc"]:
            lines.append(f"  {b['desc']}")
    return "\n".join(lines)


def to_html(bookmarks: list[dict], css_href: str) -> str:
    items = []
    for b in bookmarks:
        title = html.escape(b["title"] or b["url"])
        url = html.escape(b["url"], quote=True)
        tagstr = (
            f" - {html.escape(','.join(b['tags']))}" if b["tags"] else ""
        )
        items.append(
            f'<li><a href="{url}">{title}</a>{tagstr}</li>'
        )
    body = "\n".join(items)
    return (
        "<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\">"
        f'<title>Bookmarks</title>\n<link rel="stylesheet" href="{html.escape(css_href, quote=True)}">'
        "</head><body>\n<ul>\n"
        f"{body}\n</ul>\n</body></html>"
    )


FORMATTERS = {
    "json": to_json,
    "markdown": to_markdown,
    "org": to_org,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--db",
        type=Path,
        default=Path.home() / ".local/share/buku/bookmarks.db",
        help="Path to buku's SQLite DB (default: ~/.local/share/buku/bookmarks.db)",
    )
    parser.add_argument(
        "--exclude",
        default="",
        help="Comma-separated list of tags to exclude, e.g. --exclude private,scratch",
    )
    parser.add_argument(
        "--include",
        default="",
        help="Comma-separated list of exact tags to include (matches any tag)",
    )
    parser.add_argument(
        "--format",
        choices=list(FORMATTERS.keys()) + ["html"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--css",
        default="static/mun.css",
        help="Path (relative or absolute) used in the <link> href for --format html "
             "(default: static/mun.css)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output file path (default: stdout)",
    )
    args = parser.parse_args()

    exclude_tags = [t.strip() for t in args.exclude.split(",") if t.strip()]
    include_tags = [t.strip() for t in args.include.split(",") if t.strip()]
    bookmarks = fetch_bookmarks(args.db, exclude_tags, include_tags)
    if args.format == "html":
        output = to_html(bookmarks, args.css)
    else:
        output = FORMATTERS[args.format](bookmarks)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"Wrote {len(bookmarks)} bookmarks to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
