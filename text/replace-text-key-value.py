import os
import re

# Define the directory to process
directory = "/Users/muneer78/Documents/GitHub/personal-site/content"  # Change as needed
file_extension = ".md"

# Define your key-value replacements
replacements = {"thoughts": "misc", "bad-parent": "bad-parents"}


def apply_replacement_to_file(filepath, replacements):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            original_content = f.read()

        modified_content = original_content
        for old_word, new_word in replacements.items():
            pattern = r"\b" + re.escape(old_word) + r"\b"
            modified_content = re.sub(pattern, new_word, modified_content)

        if original_content != modified_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(modified_content)
            print(f"Modified: {filepath}")

    except Exception as e:
        print(f"Error processing file {filepath}: {e}")


def perform_replacements(directory, replacements, file_extension):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(file_extension):
                filepath = os.path.join(root, filename)
                apply_replacement_to_file(filepath, replacements)


if __name__ == "__main__":
    perform_replacements(directory, replacements, file_extension)
    print("Replacement complete.")
