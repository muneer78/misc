import os

# Set the directory where the files are located
directory = '/Users/muneer78/quartz/content/'  # Replace with the actual directory path

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".md"):  # Process only markdown files
        file_path = os.path.join(directory, filename)

        try:
            # Read the file content with error handling for encoding issues
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

            # Replace instances of "greatlines" with "great-lines"
            new_content = content.replace("covid", "great-lines")

            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)

            print(f"Updated {filename}")

        except Exception as e:
            print(f"Failed to update {filename}: {e}")

print("All files have been updated.")