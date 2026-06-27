#!/usr/bin/env python3
"""
AVERY 5160 Label Printer
Extracts addresses from a PDF and generates print-ready labels.

Usage:
    python avery_label_printer.py <pdf_path> [--output OUTPUT_PATH] [--no-open]
    python avery_label_printer.py "path/to/Voter Contact Addresses.pdf"
"""

import sys
import argparse
import webbrowser
from pathlib import Path
from typing import List

import pdfplumber
from pylabels import Specification, Sheet
from reportlab.pdfgen import shapes


def extract_addresses(pdf_path: str) -> List[str]:
    """
    Extract addresses from PDF table.
    Assumes table format: Name | Street | City | State | Zip
    """
    addresses = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue
            
            # Process rows, skipping the header (row 0)
            for row in table[1:]:
                # Mapping: 1:Name, 2:Street, 3:City, 4:State, 5:Zip
                if len(row) >= 6 and row[1]:
                    name = str(row[1]).strip()
                    street = str(row[2]).strip()
                    city = str(row[3]).strip()
                    state = str(row[4]).strip()
                    zip_code = str(row[5]).strip()
                    
                    # Create address block
                    address = f"{name}\n{street}\n{city}, {state} {zip_code}"
                    addresses.append(address)
    
    return addresses


def draw_label(label, width, height, address):
    """
    Draw a single address label.
    
    Args:
        label: ReportLab Drawing object
        width: Label width in points
        height: Label height in points
        address: Address text (multi-line string)
    """
    # Split address into lines
    lines = address.split('\n')
    
    # Font settings
    # font_name = "Helvetica"  # Customize font here
    # font_size = 8            # Customize font size here
    font_name = "Helvetica"
    font_size = 8
    line_height = 10  # points
    
    # Calculate starting y position for vertical centering
    total_text_height = len(lines) * line_height
    start_y = (height / 2) + (total_text_height / 2)
    
    # Draw each line, centered
    for idx, line in enumerate(lines):
        y = start_y - (idx * line_height)
        label.add(
            shapes.String(
                width / 2,
                y,
                line,
                fontName=font_name,
                fontSize=font_size,
                textAnchor="middle"
            )
        )


def main():
    parser = argparse.ArgumentParser(
        description="Extract addresses from PDF and generate AVERY 5160 labels"
    )
    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output PDF file path (default: ~/Downloads/avery-labels.pdf)",
        default=str(Path.home() / "Downloads" / "avery-labels.pdf")
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Don't open in browser after generating"
    )
    
    args = parser.parse_args()
    
    # Validate PDF exists
    pdf_file = Path(args.pdf_path)
    if not pdf_file.exists():
        print(f"Error: PDF file not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"📄 Reading PDF: {args.pdf_path}")
    addresses = extract_addresses(str(pdf_file))
    
    if not addresses:
        print("⚠️  No addresses found in PDF", file=sys.stderr)
        sys.exit(1)
    
    print(f"✓ Extracted {len(addresses)} addresses")
    
    # ============================================================================
    # AVERY 5160 Label Specifications (hardcoded)
    # Labels: 2.625" wide × 1" tall
    # Layout: 3 columns × 10 rows = 30 per page
    # Margins: Top 0.5", Side 0.1875"
    # ============================================================================
    # To customize for a different label format, change these values:
    # page_width=215.9,    # 8.5" in mm (Letter width)
    # page_height=279.4,   # 11" in mm (Letter height)
    # columns=3,           # Labels across
    # rows=10,             # Labels down
    # left_margin=4.76,    # 0.1875" in mm
    # top_margin=12.7,     # 0.5" in mm
    # ============================================================================
    specs = Specification(
        page_width=215.9,
        page_height=279.4,
        columns=3,
        rows=10,
        left_margin=4.76,
        top_margin=12.7,
        column_gap=0,
        row_gap=0
    )
    
    # Create sheet and add labels
    sheet = Sheet(specs, draw_label, border=True)
    
    for address in addresses:
        sheet.add_label(address)
    
    # Save to file
    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(str(output_file))
    
    print(f"✓ Generated labels: {output_file}")
    
    # Open in browser
    if not args.no_open:
        file_url = output_file.as_uri()
        print(f"🌐 Opening in browser...")
        webbrowser.open(file_url)
        print(f"💡 Ready to print! Use Cmd+P to print.")
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
