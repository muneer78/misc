import os


def remove_text_from_markdown_files(directory):
    text_to_remove = "---\ncategories: city-pics\n---\n\n"

    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            print(f"Processing file: {filepath}")

            # Read the existing content of the file
            with open(filepath, "r", encoding="utf-8") as file:
                existing_content = file.read()

            # Check if the text to remove is at the end of the content
            if existing_content.endswith(text_to_remove):
                # Remove the text from the end
                new_content = existing_content[: -len(text_to_remove)]

                # Write the modified content back to the file
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(new_content)

                print(f"Updated file: {filepath}")
            else:
                print(f"No text to remove in file: {filepath}")


if __name__ == "__main__":
    directory = "/Users/muneer78/Documents/GitHub/muneer78.github.io/_posts"  # Set the directory path here
    remove_text_from_markdown_files(directory)
