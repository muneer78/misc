import os

# Define the directory containing the files
directory = "/Users/muneer78/Desktop/test"

# Define the output Markdown file
output_md_file = "capitalized_titles_output.md"

# Store the filenames and capitalized titles in a list
capitalized_titles = []

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".md"):  # Process only .md files
        filepath = os.path.join(directory, filename)

        # Read the file content
        with open(filepath, "r") as file:
            lines = file.readlines()

        # Process each line
        updated_lines = []
        for line in lines:
            if line.startswith("title: "):
                # Extract text after "title: " and apply capitalize()
                title_text = line[len("title: ") :].strip()
                capitalized_title = title_text.capitalize()

                # Store the filename and capitalized title in the list
                capitalized_titles.append((filename, capitalized_title))

                # Reconstruct the line with the capitalized title
                updated_line = f"title: {capitalized_title}\n"
                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)

        # Write the updated content back to the file
        with open(filepath, "w") as file:
            file.writelines(updated_lines)

# Sort the capitalized titles by filename
capitalized_titles.sort(key=lambda x: x[0])

# Open the Markdown file for writing
with open(output_md_file, "w") as md_file:
    # Print the sorted capitalized titles
    for filename, capitalized_title in capitalized_titles:
        # Print to console
        print(f"File: {filename} - Capitalized title: {capitalized_title}")

        # Write to the Markdown file
        md_file.write(f"## File: {filename}\n")
        md_file.write(f"- Capitalized title: {capitalized_title}\n\n")

print(
    "Title capitalization completed and output saved to 'capitalized_titles_output.md'."
)
