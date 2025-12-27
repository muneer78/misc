import re
import os


def extract_title_from_filename(filename):
    """Extracts the title from a filename based on the date format YYYY-MM-DD."""
    match = re.search(r"\d{4}-\d{2}-\d{2}(.*)\.md$", filename)
    if match:
        return match.group(1).strip().replace("-", " ").title()
    else:
        return None


def insert_title_in_yaml_front_matter(filename):
    """Inserts the extracted title into the YAML front matter of a markdown file."""
    with open(filename, "r+") as f:
        content = f.read()

        # Check if YAML front matter exists
        if not content.startswith("---"):
            return

        # Extract title from filename
        title = extract_title_from_filename(filename)
        if not title:
            return

        # Check if title already exists in front matter
        title_match = re.search(r'title:\s*"(.*?)"\s*', content)
        if title_match:
            # Title already exists, do nothing
            return

        # Find existing tags
        tags_match = re.search(r"^tags:\s*\[(.*)\]$", content, flags=re.MULTILINE)
        tags = f"\n{tags_match.group(0)}" if tags_match else ""

        # Construct new YAML front matter with title and tags
        new_front_matter = f"---\ntitle: {title}{tags}\n---\n"

        # Replace existing front matter with new one
        content = re.sub(r"---\s*([\s\S]*?)\s*---", new_front_matter, content, count=1)

        # Remove dashes between words in title (excluding tags)
        content = re.sub(r"(?<!tags:)title: .*- ", "title: ", content)

        # Write updated content back to file
        f.seek(0)
        f.write(content)
        f.truncate()


# Example usage
directory = "/Users/muneer78/Desktop/saved/"
for filename in os.listdir(directory):
    if filename.endswith(".md"):
        insert_title_in_yaml_front_matter(os.path.join(directory, filename))
