import os

# Define the directory containing the files
directory = "/Users/muneer78/Desktop/saved/"

# Get a list of all files in the directory
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


# Function to read file content with a fallback for encoding errors
def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            return file.readlines()


# Iterate over each file and update its content
for filename in files:
    print(f"Processing file: {filename}")

    # Construct full file path
    file_path = os.path.join(directory, filename)

    # Extract title from the filename
    if "great-lines-" in filename:
        file_base, file_ext = os.path.splitext(filename)
        title_parts = file_base.split("great-lines-", 1)[1].replace("-", " ")
        title = title_parts.title()
        full_title = f"Great Lines: {title}"
        print(f"Generated title: {full_title}")

        # Read the content of the file
        content = read_file_content(file_path)

        # Prepare the new content to add at the top
        new_header = f'---\ncategories: great-lines\ntitle: "{full_title}"\n---\n'

        # Combine the new header with the existing content
        updated_content = [new_header] + content

        # Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(updated_content)

        print(f"Updated file: {filename}")
    else:
        print(f"Skipping file: {filename}, no 'great-lines-' in filename")

print("File processing complete.")
