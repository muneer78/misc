from pathlib import Path

# File paths
input_md = Path("/Users/muneer78/Downloads/links-gh.md")  # Input Markdown file
output_html = Path("/Users/muneer78/Downloads/links-gh.html")  # Output HTML file

# Read the Markdown file
with input_md.open("r", encoding="utf-8") as file:
    lines = file.readlines()

# Start building the Netscape HTML structure
html_content = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>

<DL><p>
"""

# Process each line in the Markdown file
for line in lines:
    line = line.strip()
    if line.startswith("- ["):  # Identify Markdown links
        try:
            # Extract the title and URL
            title_start = line.find("[") + 1
            title_end = line.find("]")
            title = line[title_start:title_end]

            url_start = line.find("(") + 1
            url_end = line.find(")")
            url = line[url_start:url_end]

            # Add the link to the HTML content
            html_content += f'    <DT><A HREF="{url}">{title}</A>\n'
        except Exception as e:
            print(f"Error processing line: {line} - {e}")

# Close the Netscape HTML structure
html_content += "</DL><p>\n"

# Write the HTML content to the output file
with output_html.open("w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Netscape HTML file saved to: {output_html}")