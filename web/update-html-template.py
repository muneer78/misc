#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import re


SYNTHWAVE_STYLE = """
<style id="synthwave-template">
:root {
    --pink: #ff7edb;
    --purple: #241b2f;
    --blue: #03edf9;
    --yellow: #fede5d;
    --offwhite: #ffffff;
    --neongreen: #72f1b8;
    --green: #72f1b8;
    --muted: #b6a9c8;
    --panel: #2a2139;
}

* {
    box-sizing: border-box;
}

html {
    font-size: 100%;
}

body {
    background: var(--purple);
    color: var(--offwhite);
    font-family: "Fira Sans", sans-serif;
    font-size: 18px;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 3rem 1.5rem;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: var(--pink);
    line-height: 1.2;
}

h1 {
    font-family: "Train One", sans-serif;
    font-size: clamp(2.2rem, 6vw, 4rem);
    color: var(--blue);
    margin: 0 0 3rem;
    padding-bottom: 1rem;
    border-bottom: 3px solid var(--pink);
    text-shadow:
        2px 2px 0 var(--pink),
        4px 4px 0 rgba(255, 126, 219, 0.2);
}

h2 {
    font-size: 1.65rem;
    margin-top: 2rem;
}

h3 {
    color: var(--yellow);
}

article {
    margin-bottom: 4rem;
    padding-bottom: 3rem;
    border-bottom: 2px solid var(--blue);
}

article > h2 {
    margin-top: 0;
    margin-bottom: 0.4rem;
}

article > h2 a {
    color: var(--pink);
    text-decoration: none;
}

article > h2 a:hover {
    color: var(--blue);
}

a {
    color: var(--blue);
    text-decoration-color: var(--pink);
    text-underline-offset: 0.2em;
}

a:hover {
    color: var(--yellow);
}

.source {
    margin-top: 0;
    margin-bottom: 2rem;
    color: var(--neongreen);
    font-family: monospace;
    font-size: 0.8rem;
    overflow-wrap: anywhere;
}

.body {
    overflow-wrap: break-word;
}

.body p {
    margin: 1.25rem 0;
}

.body h2 {
    color: var(--yellow);
    margin-top: 2.5rem;
}

.body h3 {
    color: var(--neongreen);
}

strong {
    color: var(--yellow);
}

em {
    color: #f3d9ef;
}

blockquote {
    margin: 2rem 0;
    padding: 0.5rem 1.5rem;
    border-left: 4px solid var(--pink);
    background: rgba(255, 126, 219, 0.06);
}

blockquote p:first-child {
    margin-top: 0.5rem;
}

blockquote p:last-child {
    margin-bottom: 0.5rem;
}

hr {
    border: 0;
    border-top: 1px solid var(--blue);
    margin: 3rem 0;
    opacity: 0.65;
}

img {
    display: block;
    max-width: 100%;
    height: auto;
    margin: 2rem auto;
}

figure {
    max-width: 100%;
    margin: 2rem 0;
}

figure button {
    display: block;
    width: 100%;
    padding: 0;
    border: 0;
    background: transparent;
}

figcaption,
.photoCaption {
    margin-top: 0.5rem;
    color: var(--muted);
    font-size: 0.85rem;
    line-height: 1.4;
}

aside {
    max-width: 100%;
}

.failed {
    padding: 1.5rem;
    border: 1px solid var(--pink);
    border-left: 5px solid var(--pink);
    background: rgba(255, 126, 219, 0.08);
}

.failed h2 {
    color: var(--pink);
}

.error {
    color: var(--yellow);
}

code,
pre {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}

code {
    color: var(--neongreen);
}

pre {
    padding: 1rem;
    overflow-x: auto;
    background: #191321;
    border-left: 4px solid var(--blue);
}

::selection {
    color: var(--purple);
    background: var(--pink);
}

@media (max-width: 600px) {
    body {
        font-size: 17px;
        padding: 2rem 1rem;
    }

    h1 {
        margin-bottom: 2rem;
    }

    article {
        margin-bottom: 3rem;
        padding-bottom: 2rem;
    }
}
</style>
""".strip()


FONT_LINK = (
    '<link rel="stylesheet" '
    'href="https://fonts.googleapis.com/css2?'
    'family=Fira+Sans:ital,wght@0,300;0,400;0,700;1,400'
    '&family=Train+One&display=swap">'
)


def update_html(path: Path, backup: bool = False) -> bool:
    html = path.read_text(encoding="utf-8")

    original = html

    # Fix malformed doctype if necessary.
    if html.lstrip().startswith("!DOCTYPE html>"):
        html = html.replace("!DOCTYPE html>", "<!DOCTYPE html>", 1)

    # Remove an existing Synthwave template from a previous run.
    html = re.sub(
        r'<style\s+id=["\']synthwave-template["\'].*?</style>',
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Remove the page's existing inline stylesheet.
    html = re.sub(
        r"<style\b[^>]*>.*?</style>",
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Avoid adding the Google Fonts link repeatedly.
    html = re.sub(
        r'<link[^>]+fonts\.googleapis\.com[^>]*>',
        "",
        html,
        flags=re.IGNORECASE,
    )

    # Insert the template immediately before </head>.
    template = f"\n{FONT_LINK}\n{SYNTHWAVE_STYLE}\n"

    html, count = re.subn(
        r"</head>",
        f"{template}</head>",
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    if count == 0:
        print(f"SKIP  {path} — no </head>")
        return False

    if html == original:
        print(f"OK    {path} — already current")
        return False

    if backup:
        backup_path = path.with_suffix(path.suffix + ".bak")

        if not backup_path.exists():
            backup_path.write_text(original, encoding="utf-8")

    path.write_text(html, encoding="utf-8")

    print(f"UPDATE {path}")
    return True


def main():
    parser = ArgumentParser(
        description="Apply the Synthwave design to article HTML pages."
    )

    parser.add_argument(
        "path",
        type=Path,
        help="HTML file or directory containing HTML files",
    )

    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create .html.bak files before modifying pages",
    )

    args = parser.parse_args()

    if not args.path.exists():
        raise SystemExit(f"Path does not exist: {args.path}")

    if args.path.is_file():
        files = [args.path]
    else:
        files = sorted(args.path.rglob("*.html"))

    if not files:
        raise SystemExit(f"No HTML files found in {args.path}")

    updated = 0

    for path in files:
        updated += update_html(path, args.backup)

    print()
    print(f"Processed: {len(files)}")
    print(f"Updated:   {updated}")
    print(f"Unchanged: {len(files) - updated}")


if __name__ == "__main__":
    main()
