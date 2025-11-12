import os

def combine_documents(script_directory):
    # Get all .md files with their full paths
    files = [
        os.path.join(script_directory, file)
        for file in os.listdir(script_directory)
        if file.endswith(".md")
    ]
    # Sort files by modification time (newest first)
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    combined_content = ""
    count, number_of_files = 0, len(files)

    for file_path in files:
        file = os.path.basename(file_path)
        with open(file_path, "r") as f:
            content = f.read()
        combined_content += f"# {file}\n\n"
        combined_content += content
        if count < number_of_files - 1:
            combined_content += "\n\n---\n\n"
        count += 1

    combined_file_path = os.path.join(script_directory, "notes.md")
    with open(combined_file_path, "w") as combined_file:
        combined_file.write(combined_content)

script_directory = r"/Users/muneer78/Downloads/docs"

if __name__ == "__main__":
    combine_documents(script_directory)