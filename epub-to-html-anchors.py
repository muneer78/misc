#!/usr/bin/env python3
"""
EPUB to HTML Converter
Converts an EPUB file into a single HTML page with anchor links for navigation.
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
        self.toc_entries = []
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

        return metadata, spine_items, base_path

    def extract_toc_from_ncx(self, zip_file, base_path):
        """Extract table of contents from NCX file."""
        try:
            # Try to find NCX file
            ncx_path = None
            if base_path:
                ncx_candidates = [f"{base_path}/toc.ncx", "toc.ncx"]
            else:
                ncx_candidates = ["toc.ncx"]

            for candidate in ncx_candidates:
                try:
                    zip_file.getinfo(candidate)
                    ncx_path = candidate
                    break
                except KeyError:
                    continue

            if not ncx_path:
                return []

            ncx_content = zip_file.read(ncx_path)
            ncx_root = ET.fromstring(ncx_content)

            toc_entries = []

            def extract_navpoints(parent, level=0):
                for navpoint in parent.findall(
                    ".//{http://www.daisy.org/z3986/2005/ncx/}navPoint"
                ):
                    # Get label
                    label_elem = navpoint.find(
                        ".//{http://www.daisy.org/z3986/2005/ncx/}text"
                    )
                    label = label_elem.text if label_elem is not None else "Untitled"

                    # Get content source
                    content_elem = navpoint.find(
                        ".//{http://www.daisy.org/z3986/2005/ncx/}content"
                    )
                    if content_elem is not None:
                        src = content_elem.get("src", "")
                        if base_path and not src.startswith(base_path):
                            src = f"{base_path}/{src}"

                        toc_entries.append({"label": label, "src": src, "level": level})

            extract_navpoints(ncx_root)
            return toc_entries

        except Exception as e:
            print(f"Warning: Could not parse NCX file: {e}")
            return []

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

    def generate_anchor_id(self, text):
        """Generate a clean anchor ID from text."""
        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)
        # Convert to lowercase and replace spaces/special chars with hyphens
        anchor_id = re.sub(r"[^\w\s-]", "", text.lower())
        anchor_id = re.sub(r"[-\s]+", "-", anchor_id)
        return anchor_id.strip("-")

    def process_epub(self):
        """Main processing function."""
        try:
            with zipfile.ZipFile(self.epub_path, "r") as zip_file:
                # Parse OPF file
                metadata, spine_items, base_path = self.parse_opf_file(zip_file)

                # Extract TOC from NCX
                toc_entries = self.extract_toc_from_ncx(zip_file, base_path)

                # Process each spine item
                for item_path in spine_items:
                    try:
                        content = zip_file.read(item_path).decode("utf-8")
                        cleaned_content = self.clean_html_content(content)

                        if cleaned_content:
                            # Find matching TOC entry
                            toc_entry = None
                            for entry in toc_entries:
                                if entry["src"].split("#")[0] == item_path:
                                    toc_entry = entry
                                    break

                            # If no TOC entry, try to extract title from content
                            if not toc_entry:
                                title_match = re.search(
                                    r"<h[1-6][^>]*>(.*?)</h[1-6]>",
                                    cleaned_content,
                                    re.IGNORECASE,
                                )
                                title = (
                                    title_match.group(1)
                                    if title_match
                                    else f"Section {len(self.content_sections) + 1}"
                                )
                                toc_entry = {"label": title, "level": 0}

                            anchor_id = self.generate_anchor_id(toc_entry["label"])

                            self.content_sections.append(
                                {
                                    "title": toc_entry["label"],
                                    "anchor_id": anchor_id,
                                    "content": cleaned_content,
                                    "level": toc_entry.get("level", 0),
                                }
                            )

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

        .toc {{
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .toc h2 {{
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}

        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}

        .toc li {{
            margin: 8px 0;
        }}

        .toc a {{
            color: #0066cc;
            text-decoration: none;
            display: block;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}

        .toc a:hover {{
            background-color: #f0f0f0;
            text-decoration: underline;
        }}

        .toc .level-1 {{ padding-left: 20px; }}
        .toc .level-2 {{ padding-left: 40px; }}
        .toc .level-3 {{ padding-left: 60px; }}

        .content {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .section {{
            margin-bottom: 40px;
            border-bottom: 1px solid #eee;
            padding-bottom: 30px;
        }}

        .section:last-child {{
            border-bottom: none;
        }}

        .section-title {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }}

        .back-to-top {{
            display: inline-block;
            margin-top: 20px;
            color: #0066cc;
            text-decoration: none;
            font-size: 0.9em;
        }}

        .back-to-top:hover {{
            text-decoration: underline;
        }}

        /* Style the actual content */
        .section-content h1,
        .section-content h2,
        .section-content h3,
        .section-content h4,
        .section-content h5,
        .section-content h6 {{
            color: #333;
            margin-top: 25px;
            margin-bottom: 15px;
        }}

        .section-content p {{
            margin-bottom: 15px;
            text-align: justify;
        }}

        .section-content img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
        }}

        .section-content blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            color: #666;
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

        # Table of Contents
        if self.content_sections:
            html_parts.append("""
    <div class="toc" id="table-of-contents">
        <h2>Table of Contents</h2>
        <ul>""")

            for section in self.content_sections:
                level_class = f"level-{min(section['level'], 3)}"
                html_parts.append(f'''
            <li class="{level_class}">
                <a href="#{section["anchor_id"]}">{escape(section["title"])}</a>
            </li>''')

            html_parts.append("""
        </ul>
    </div>""")

        # Content sections
        html_parts.append('    <div class="content">')

        for section in self.content_sections:
            html_parts.append(f'''
        <div class="section" id="{section["anchor_id"]}">
            <h2 class="section-title">{escape(section["title"])}</h2>
            <div class="section-content">
                {section["content"]}
            </div>
            <a href="#table-of-contents" class="back-to-top">↑ Back to Top</a>
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
            print(f"Generated {len(self.content_sections)} sections with navigation")
        except Exception as e:
            print(f"Error writing HTML file: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Convert EPUB file to HTML with anchor navigation"
    )
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
