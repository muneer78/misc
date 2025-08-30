def process_markdown(filename):
    with open(filename, "r") as file:
        content = file.readlines()

    for i, line in enumerate(content):
        if line.startswith("#"):
            # Extract the first word prefixed by #
            parts = line.strip().split()
            # Rejoin the words with #
            modified_line = "#".join(parts)
            # Replace the original line with the modified one
            content[i] = modified_line + "\n"
            break  # Stop after modifying the first line with #

    with open(filename, "w") as file:
        file.writelines(content)


# Replace 'your_file.md' with the path to your Markdown file
process_markdown("/Users/muneer78/Downloads/links.md")
