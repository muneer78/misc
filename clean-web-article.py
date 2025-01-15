import re
from pathlib import Path

def clean_markdown(file_path):
    file_path = Path(file_path)
    lines = file_path.read_text().splitlines()

    cleaned_lines = []
    blank_line_count = 0

    for line in lines:
        # Remove lines where the only word begins with 'ad'
        if re.match(r'^\s*ad\w*\s*$', line.strip(), re.IGNORECASE):
            continue
        # Remove lines where the only word begins with 'Read More'
        if re.match(r'^\s*Read More\w*\s*$', line.strip(), re.IGNORECASE):
            continue
        # Remove lines that begin with HTML tags
        if re.match(r'^\s*<[^>]+>', line.strip()):
            continue
        # Remove image links
        if re.match(r'!\[.*\]\(.*\)', line.strip()):
            continue
        # Reduce multiple blank lines to a single blank line
        if line.strip() == "":
            blank_line_count += 1
            if blank_line_count > 1:
                continue
        else:
            blank_line_count = 0

        cleaned_lines.append(line)

    # Create the new file name
    new_file_path = file_path.with_name(f"{file_path.stem}-cleaned{file_path.suffix}")

    new_file_path.write_text('\n'.join(cleaned_lines))

# Replace with the path to your markdown file
clean_markdown(r'/Users/muneer78/Downloads/The Singular Mind of Terry Tao - The New York Times.md')

print("Markdown file cleaned successfully!")