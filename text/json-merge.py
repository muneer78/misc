from pathlib import Path
import json


def delete_first_line(file_path):
    with file_path.open("r", encoding="utf-8") as file:
        lines = file.readlines()[1:]  # Skip the first line
    with file_path.open("w", encoding="utf-8") as file:
        file.writelines(lines)


def merge_json_files(directory, output_file, non_json_file):
    directory_path = Path(directory)

    if not directory_path.exists():
        print(f"Directory does not exist: {directory}")
        exit(1)

    merged_data = []
    non_json_content = []

    for file_path in directory_path.iterdir():
        if file_path.suffix.lower() == ".json":
            delete_first_line(file_path)
            try:
                with file_path.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                    merged_data.append(data)
            except json.JSONDecodeError:
                print(f"Non-JSON content found in file: {file_path}")
                non_json_content.append(file_path)

    # Write non-JSON files content to a separate file
    with Path(non_json_file).open("w", encoding="utf-8") as non_json_outfile:
        for file_path in non_json_content:
            with file_path.open("r", encoding="utf-8") as file:
                non_json_outfile.write(file.read())
            non_json_outfile.write("\n\n")

    # Write merged JSON data to the output file
    with Path(output_file).open("w", encoding="utf-8") as outfile:
        json.dump(merged_data, outfile, indent=4)


directory = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\json"
output_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\merged_output.json"
non_json_file = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\non_json_content.txt"
merge_json_files(directory, output_file, non_json_file)
