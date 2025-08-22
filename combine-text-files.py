import os


def combine_documents(script_directory):
    # Get all text files in the script's directory
    files = [file for file in os.listdir(script_directory) if file.endswith(".txt")]

    combined_content = ""

    count, number_of_files = 0, len(files)

    for file in files:
        file_path = os.path.join(script_directory, file)

        # Read the content of each text file
        with open(file_path, "r") as f:
            content = f.read()

        # Add the filename as a title for each new section
        combined_content += f"# {file}\n\n"

        # Append the content of the text file
        combined_content += content

        # Don't add a page break if it's the last file
        if count < number_of_files - 1:
            combined_content += "\n\n---\n\n"

        count += 1

    # Save the combined content to a new text file
    combined_file_path = os.path.join(script_directory, "bft.txt")
    with open(combined_file_path, "w") as combined_file:
        combined_file.write(combined_content)


script_directory = r"/Users/muneer78/Desktop/text"

if __name__ == "__main__":
    combine_documents(script_directory)
