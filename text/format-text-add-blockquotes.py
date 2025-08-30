import os
from pathlib import Path


def add_blockquote_to_md(file_path):
    """
    Adds a Markdown blockquote character ('> ') to the beginning of each line
    in a given Markdown file and saves the result to a new file named
    '[original_filename]_v2.md'.

    Args:
        file_path (str): The path to the Markdown file.
    """
    try:
        original_path = Path(file_path)

        # Check if the original file exists
        if not original_path.is_file():
            print(f"Error: The file '{file_path}' was not found.")
            return

        # Construct the new file path
        # Example: 'my_document.md' becomes 'my_document_v2.md'
        new_file_name = f"{original_path.stem}_v2{original_path.suffix}"
        new_file_path = original_path.parent / new_file_name

        # Read the original content of the file
        with open(original_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Prepend '> ' to each line
        modified_lines = [f"> {line}" for line in lines]

        # Write the modified content to the new file
        with open(new_file_path, "w", encoding="utf-8") as f:
            f.writelines(modified_lines)

        print(f"Successfully added blockquotes and saved to '{new_file_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")


# --- How to use this script ---
# Example usage:
# If your markdown file is named 'my_document.md' and is in the same directory
# as this script, you would call:
add_blockquote_to_md("/Users/muneer78/Downloads/darnold.md")

# If your file is in a different path, provide the full path:
# add_blockquote_to_md('/path/to/your/documents/another_file.md')

# Replace 'your_markdown_file.md' with the actual path to your file
# For demonstration purposes, let's assume a file named 'example.md' exists.
# You would uncomment the line below and replace the placeholder:
# add_blockquote_to_md('your_markdown_file.md')

# To test, you can create a dummy file first:
# with open('test_file.md', 'w', encoding='utf-8') as f:
#     f.write("This is line 1.\n")
#     f.write("This is line 2.\n")
#     f.write("And a final line.")

# Then call the function:
# add_blockquote_to_md('test_file.md')
# After running, a new file named 'test_file_v2.md' will be created
# with blockquotes added.
