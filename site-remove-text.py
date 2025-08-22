import os
import csv
import re


def extract_tags_and_filenames_from_csv(csv_filepath):
    file_tag_map = {}
    with open(csv_filepath, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = row["finaltitle"]
            tags = row["tags"].split(",")
            file_tag_map[filename] = tags
    return file_tag_map


def update_markdown_files(directory, file_tag_map):
    not_updated_files = []
    category_pattern = re.compile(r"^---\ncategories:.*?\n---\n\n", re.DOTALL)

    # Iterate over the filenames to update
    for filename, tags in file_tag_map.items():
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith(".md"):
            print(f"Processing file: {filepath}")

            categories_value = "categories: " + ", ".join(tags)
            new_text = f"---\n{categories_value}\n---\n\n"

            # Read the existing content of the file
            with open(filepath, "r", encoding="utf-8") as file:
                existing_content = file.read()

            # Remove existing categories block if present
            existing_content = category_pattern.sub("", existing_content)

            # Combine the new text with the existing content
            new_content = new_text + existing_content

            # Write the modified content back to the file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_content)

            print(f"Updated file: {filepath}")
        else:
            not_updated_files.append(filename)
            print(f"File not found or not a markdown file: {filepath}")

    return not_updated_files


def write_not_updated_files_csv(not_updated_files, output_csv_filepath):
    with open(output_csv_filepath, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["not_updated_files"])
        for filename in not_updated_files:
            writer.writerow([filename])


if __name__ == "__main__":
    directory = "/Users/muneer78/Documents/GitHub/muneer78.github.io/_posts"  # Set the directory path here
    csv_filepath = "/Users/muneer78/Downloads/updated_file_cats_final.csv"  # Set the CSV file path here
    output_csv_filepath = "/Users/muneer78/Desktop/not_updated_files.csv"  # Set the output CSV file path here

    file_tag_map = extract_tags_and_filenames_from_csv(csv_filepath)
    not_updated_files = update_markdown_files(directory, file_tag_map)
    write_not_updated_files_csv(not_updated_files, output_csv_filepath)
