#!/usr/bin/env python3
"""
EPUB to HTML Converter (Simple Version)
Converts an EPUB file into a single HTML page without anchor navigation.
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import argparse
import sys
from html import escape


class EpubToHtmlConverter:
    def __init__(self, epub_path, output_path=None):
        self.epub_path = Path(epub_path)
        self.output_path = (
            Path(output_path) if output_path else self.epub_path.with_suffix(".html")
        )
        self.namespaces = {
            "opf": "http://www.idpf.org/2007/opf",
            "dc": "http://purl.org/dc/elements/1.1/",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        self.content_sections = []

    def extract_metadata(self, opf_root):
        """Extract book metadata from OPF file."""
        metadata = {}

        # Get title
        title_elem = opf_root.find(".//dc:title", self.namespaces)
        metadata["title"] = (
            title_elem.text if title_elem is not None else "Unknown Title"
        )

        # Get author
        author_elem = opf_root.find(".//dc:creator", self.namespaces)
        metadata["author"] = (
            author_elem.text if author_elem is not None else "Unknown Author"
        )

        # Get description
        desc_elem = opf_root.find(".//dc:description", self.namespaces)
        metadata["description"] = desc_elem.text if desc_elem is not None else ""

        return metadata

    def parse_opf_file(self, zip_file):
        """Parse the OPF file to get spine order and manifest."""
        # Find container.xml to locate OPF file
        container_content = zip_file.read("META-INF/container.xml")
        container_root = ET.fromstring(container_content)

        opf_path = None
        for rootfile in container_root.findall(
            ".//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile"
        ):
            if rootfile.get("media-type") == "application/oebps-package+xml":
                opf_path = rootfile.get("full-path")
                break

        if not opf_path:
            raise ValueError("Could not find OPF file in EPUB")

        # Parse OPF file
        opf_content = zip_file.read(opf_path)
        opf_root = ET.fromstring(opf_content)

        # Get base path for relative references
        base_path = str(Path(opf_path).parent)

        # Extract metadata
        metadata = self.extract_metadata(opf_root)

        # Build manifest (id -> href mapping)
        manifest = {}
        for item in opf_root.findall(".//opf:item", self.namespaces):
            item_id = item.get("id")
            href = item.get("href")
            if base_path and base_path != ".":
                href = f"{base_path}/{href}"
            manifest[item_id] = href

        # Get spine order
        spine_items = []
        for itemref in opf_root.findall(".//opf:itemref", self.namespaces):
            idref = itemref.get("idref")
            if idref in manifest:
                spine_items.append(manifest[idref])

        return metadata, spine_items

    def clean_html_content(self, content):
        """Clean and process HTML content."""
        # Remove XML namespace declarations
        content = re.sub(r'xmlns[^=]*="[^"]*"', "", content)

        # Remove DOCTYPE if present
        content = re.sub(r"<!DOCTYPE[^>]*>", "", content)

        # Extract body content if full HTML document
        body_match = re.search(
            r"<body[^>]*>(.*?)</body>", content, re.DOTALL | re.IGNORECASE
        )
        if body_match:
            content = body_match.group(1)

        # Clean up extra whitespace
        content = re.sub(r"\n\s*\n", "\n\n", content)

        return content.strip()

    def process_epub(self):
        """Main processing function."""
        try:
            with zipfile.ZipFile(self.epub_path, "r") as zip_file:
                # Parse OPF file
                metadata, spine_items = self.parse_opf_file(zip_file)

                # Process each spine item
                for item_path in spine_items:
                    try:
                        content = zip_file.read(item_path).decode("utf-8")
                        cleaned_content = self.clean_html_content(content)

                        if cleaned_content:
                            self.content_sections.append(cleaned_content)

                    except Exception as e:
                        print(f"Warning: Could not process {item_path}: {e}")
                        continue

                # Generate HTML output
                self.generate_html_output(metadata)

        except Exception as e:
            print(f"Error processing EPUB: {e}")
            sys.exit(1)

    def generate_html_output(self, metadata):
        """Generate the final HTML output."""
        html_parts = []

        # HTML header
        html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(metadata["title"])}</title>
    <style>
        body {{
            font-family: Georgia, serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fafafa;
            color: #333;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            color: #333;
            margin-bottom: 10px;
        }}

        .header .author {{
            color: #666;
            font-style: italic;
            margin-bottom: 15px;
        }}

        .header .description {{
            color: #666;
            line-height: 1.4;
        }}

        .content {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .section {{
            margin-bottom: 40px;
            padding-bottom: 30px;
        }}

        .section:not(:last-child) {{
            border-bottom: 1px solid #eee;
        }}

        /* Style the content elements */
        h1, h2, h3, h4, h5, h6 {{
            color: #333;
            margin-top: 30px;
            margin-bottom: 15px;
            line-height: 1.3;
        }}

        h1 {{
            font-size: 2em;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}

        h2 {{
            font-size: 1.5em;
        }}

        h3 {{
            font-size: 1.3em;
        }}

        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}

        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 4px;
        }}

        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            color: #666;
        }}

        pre {{
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
        }}

        code {{
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}

        ul, ol {{
            margin-bottom: 15px;
            padding-left: 30px;
        }}

        li {{
            margin-bottom: 5px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}

        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}

        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        .page-break {{
            page-break-before: always;
            margin-top: 50px;
            border-top: 2px solid #eee;
            padding-top: 30px;
        }}

        @media print {{
            body {{
                background: white;
                font-size: 12pt;
            }}

            .header, .content {{
                box-shadow: none;
                border: none;
            }}
        }}
    </style>
</head>
<body>""")

        # Header section
        html_parts.append(f"""
    <div class="header">
        <h1>{escape(metadata["title"])}</h1>
        <div class="author">by {escape(metadata["author"])}</div>
        {f'<p class="description">{escape(metadata["description"])}</p>' if metadata["description"] else ""}
    </div>""")

        # Content sections
        html_parts.append('    <div class="content">')

        for i, section_content in enumerate(self.content_sections):
            # Add page break class for sections after the first
            section_class = "section"
            if i > 0:
                section_class += " page-break"

            html_parts.append(f'''
        <div class="{section_class}">
            {section_content}
        </div>''')

        html_parts.append("    </div>")

        # Close HTML
        html_parts.append("""
</body>
</html>""")

        # Write to file
        final_html = "\n".join(html_parts)

        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(final_html)
            print(f"Successfully converted '{self.epub_path}' to '{self.output_path}'")
            print(f"Generated HTML with {len(self.content_sections)} sections")
        except Exception as e:
            print(f"Error writing HTML file: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Convert EPUB file to simple HTML")
    parser.add_argument("epub_file", help="Path to the EPUB file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output HTML file path (default: same name as EPUB with .html extension)",
    )

    args = parser.parse_args()

    if not Path(args.epub_file).exists():
        print(f"Error: EPUB file '{args.epub_file}' not found")
        sys.exit(1)

    converter = EpubToHtmlConverter(args.epub_file, args.output)
    converter.process_epub()


if __name__ == "__main__":
    main()
