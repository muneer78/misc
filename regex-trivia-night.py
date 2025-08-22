import os
import re


def apply_regex_replacements(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # Apply the regex replacements
    content = re.sub(r"^###\s*Notes:\s*\n\s*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"<!--\s*Slide number:\s*\d+\s*-->", "---\n", content)
    content = re.sub(
        r"\n{2,}", "\n", content
    )  # Remove one newline if there are two consecutive newlines
    content = re.sub(r"^(#.*)$", r"\1\n", content, flags=re.MULTILINE)

    # Add a number and period at the beginning of each line after '# Round * Answers' until '---' is found
    def add_numbering(match):
        lines = match.group(2).strip().split("\n")
        numbered_lines = [f"{i + 1}. {line}" for i, line in enumerate(lines)]
        return match.group(1) + "\n".join(numbered_lines) + match.group(3)

    content = re.sub(
        r"(# Round\s*\d*\s*Answers\n)(.*?)(\n---)",
        add_numbering,
        content,
        flags=re.DOTALL,
    )

    with open(file_path, "w") as file:
        file.write(content)


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                apply_regex_replacements(file_path)
                print(f"Processed {file_path}")


if __name__ == "__main__":
    directory = "/Users/muneer78/Downloads/convert"
    process_directory(directory)
