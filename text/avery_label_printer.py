#!/usr/bin/env python3
"""
AVERY 5160 Label Printer
Extracts addresses from a PDF and generates print-ready labels as a PDF.

Usage:
    python avery_label_printer.py <pdf_path> [--output OUTPUT_PATH] [--no-open]
    python avery_label_printer.py "path/to/Voter Contact Addresses.pdf"
    python avery_label_printer.py "path/to/addresses.pdf" --output ~/Downloads/labels.pdf
"""

import sys
import argparse
import webbrowser
from pathlib import Path
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import pdfplumber


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


def generate_pdf(addresses: List[str], output_path: str) -> None:
    """
    Generate print-ready PDF for AVERY 5160 labels.
    AVERY 5160: 10 rows × 3 columns, 1" × 2.625" per label
    """
    
    if not addresses:
        print("Error: No addresses to print", file=sys.stderr)
        return
    
    # AVERY 5160 dimensions (in inches)
    # Labels are 2.625" wide x 1" tall (3 columns x 10 rows = 30 per page)
    PAGE_WIDTH, PAGE_HEIGHT = letter
    LABEL_WIDTH = 2.625 * inch
    LABEL_HEIGHT = 1.0 * inch
    LABELS_PER_ROW = 3
    LABELS_PER_COL = 10
    LABELS_PER_PAGE = LABELS_PER_ROW * LABELS_PER_COL
    
    # Margins
    TOP_MARGIN = 0.5 * inch
    LEFT_MARGIN = 0.1875 * inch
    
    # Create PDF
    pdf_canvas = canvas.Canvas(output_path, pagesize=letter)
    
    # Process addresses in batches of 30 (one page at a time)
    for page_num in range(0, len(addresses), LABELS_PER_PAGE):
        page_addresses = addresses[page_num:page_num + LABELS_PER_PAGE]
        
        # Draw labels on this page
        for label_idx, address in enumerate(page_addresses):
            # Calculate position (row, col)
            row = label_idx // LABELS_PER_ROW
            col = label_idx % LABELS_PER_ROW
            
            # Calculate x, y position
            x = LEFT_MARGIN + (col * LABEL_WIDTH)
            y = PAGE_HEIGHT - TOP_MARGIN - ((row + 1) * LABEL_HEIGHT)
            
            # Draw label border
            pdf_canvas.rect(x, y, LABEL_WIDTH, LABEL_HEIGHT, stroke=1, fill=0)
            
            # Draw centered text in label
            text_lines = address.split('\n')
            
            # For narrower labels, use smaller font
            pdf_canvas.setFont("Helvetica", 8)
            
            # Calculate vertical centering (labels are only 1" tall)
            line_height = 9  # points
            total_text_height = len(text_lines) * line_height
            start_y = y + (LABEL_HEIGHT / 2) + (total_text_height / 2)
            
            # Draw each line of the address, centered
            for line_idx, line in enumerate(text_lines):
                line_y = start_y - (line_idx * line_height)
                # Center horizontally within the label
                text_width = pdf_canvas.stringWidth(line, "Helvetica", 8)
                text_x = x + (LABEL_WIDTH / 2) - (text_width / 2)
                pdf_canvas.drawString(text_x, line_y, line)
        
        # New page for next batch
        pdf_canvas.showPage()
    
    pdf_canvas.save()


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
    
    # Generate PDF
    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    generate_pdf(addresses, str(output_file))
    
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
