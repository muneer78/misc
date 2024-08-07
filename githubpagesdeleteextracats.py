import os
import re

def clean_markdown_files(directory):
    # Define the block to remove
    block_to_remove = '---\ncategories: great-lines\n---\n'
    block_pattern = re.compile(re.escape(block_to_remove), re.MULTILINE | re.DOTALL)

    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            print(f"Processing file: {filepath}")

            # Read the existing content of the file
            with open(filepath, 'r', encoding='utf-8') as file:
                existing_content = file.read()

            # Remove only the first occurrence of the block
            new_content = block_pattern.sub('', existing_content, count=1)

            # Write the modified content back to the file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_content)

            print(f"Updated file: {filepath}")
if __name__ == "__main__":
    directory = '/Users/muneer78/Documents/GitHub/muneer78.github.io/_posts'  # Set the directory path here
    clean_markdown_files(directory)
