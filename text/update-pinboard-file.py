import re


def reformat_file(filename):
    with open(filename, "r") as file:
        content = file.read()

    # Regular expression to match the pattern and capture the href, description, and tag
    pattern = r'<post href="([^"]+)"[^>]+description="([^"]+)"[^>]+tag="([^"]+)"[^>]+hash="[^"]+" */?>'

    # Function to reformat the matched content
    def reformat_match(match):
        href = match.group(1)
        description = match.group(2)
        tags = match.group(3).split(",")
        # Add # before each tag
        formatted_tags = " ".join(f"#{tag.strip()}" for tag in tags)
        return f"[{description}]({href}) {formatted_tags}"

    # Substitute all matches in the content
    new_content = re.sub(pattern, reformat_match, content)

    # Optionally write the reformatted content to a new file
    with open(filename, "w") as file:
        file.write(new_content)


# Use the function
reformat_file("/Users/muneer78/Downloads/pinboard_export.2024.09.28_15.14.xml")
