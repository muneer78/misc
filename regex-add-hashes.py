import re


def add_tags(text):
    pattern = r"\]\s+(\w+)"
    matches = re.finditer(pattern, text)

    modified_text = []
    last_end = 0

    for match in matches:
        start, end = match.span()
        modified_text.extend(text[last_end:start].split())
        modified_text.append(text[start:end])
        for word in text[end:].split():
            if not word.startswith("#"):
                word = "#" + word
            modified_text.append(word)
        last_end = end + len(word) + 1  # Adjust for trailing whitespace

    modified_text.extend(text[last_end:].split())
    return "\n".join(modified_text)


# Replace 'input.txt' and 'output.txt' with your actual file names
with (
    open(r"/Users/muneer78/Downloads/pinboard.txt", "r") as f,
    open(r"/Users/muneer78/Downloads/pinboard_output.txt", "w") as out,
):
    text = f.read()
    modified_text = add_tags(text)
    out.write(modified_text)
