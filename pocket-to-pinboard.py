from datetime import datetime
from pathlib import Path

# File paths
input_md = Path("/Users/muneer78/Documents/GitHub/muneer78.github.io/_links/2025-04-18-instapaper.md")  # Input Markdown file
output_html = Path("/Users/muneer78/data/instapaper.html")  # Output HTML file

# Read the Markdown file and extract data
bookmarks = []
with open(input_md, "r", encoding="utf-8") as mdfile:
    lines = mdfile.readlines()

# Process each line in the Markdown file
for line in lines:
    line = line.strip()
    if line.startswith("- "):  # Process only list items
        try:
            # Extract the date, title, and URL
            date, rest = line[2:].split(": ", 1)
            title, url = rest.split("](", 1)
            title = title.strip("[")
            url = url.strip(")")
            add_date = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
            bookmarks.append((title, url, add_date))
        except ValueError:
            continue  # Skip lines that don't match the expected format

# Generate the HTML content
html_content = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Pocket Bookmarks</TITLE>
<H1>Pocket Bookmarks</H1>

<DL><p>
    <DT><H3 ADD_DATE="{add_date}" LAST_MODIFIED="{last_modified}" PERSONAL_TOOLBAR_FOLDER="true">Pocket Saved Items</H3>
    <DL><p>
""".format(
    add_date=int(datetime.now().timestamp()),
    last_modified=int(datetime.now().timestamp()),
)

# Add bookmarks to the HTML content
for title, url, add_date in bookmarks:
    html_content += f'        <DT><A HREF="{url}" ADD_DATE="{add_date}">{title}</A>\n'

# Close the HTML structure
html_content += """    </DL><p>
</DL>
"""

# Write the HTML content to a file
with open(output_html, "w", encoding="utf-8") as htmlfile:
    htmlfile.write(html_content)

print(f"HTML file created: {output_html}")