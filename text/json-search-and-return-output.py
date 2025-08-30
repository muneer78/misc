from pathlib import Path
import json
import csv


def search_json_files(directory, search_string, output_csv):
    found_json = False  # Flag to track if any JSON files are found
    found_match = False  # Flag to track if any match is found
    matches = []  # List to store matches as dictionaries for CSV writing

    # Convert directory to Path object
    directory_path = Path(directory)

    # Walk through the directory
    for file_path in directory_path.rglob(
        "*.json"
    ):  # Search for JSON files recursively
        found_json = True
        try:
            with file_path.open("r", encoding="utf-8") as f:
                # Read the entire content of the file
                file_content = f.read()
                # Find all valid JSON substrings in the content
                json_strings = file_content.splitlines()
                for json_string in json_strings:
                    try:
                        data = json.loads(json_string)
                        if isinstance(data, dict):
                            # If data is a dictionary
                            for key, value in data.items():
                                if isinstance(value, str) and search_string in value:
                                    match = {
                                        "file": str(file_path),
                                        "key": key,
                                        "value": value,
                                    }
                                    matches.append(match)
                                    found_match = True
                        elif isinstance(data, list):
                            # If data is a list
                            for item in data:
                                if isinstance(item, dict):
                                    for key, value in item.items():
                                        if (
                                            isinstance(value, str)
                                            and search_string in value
                                        ):
                                            match = {
                                                "file": str(file_path),
                                                "key": key,
                                                "value": value,
                                            }
                                            matches.append(match)
                                            found_match = True
                    except json.JSONDecodeError:
                        # Skip over non-JSON parts of the file
                        pass
        except Exception as e:
            print(f"Error processing file: {file_path} - {e}")

    if not found_json:
        print("No JSON files in directory")
    elif not found_match:
        print("Search term not found")
    else:
        # Print matches to the console
        for match in matches:
            print(
                f"Found match in file: {match['file']} | Key: {match['key']} | Value: {match['value']}"
            )

        # Write matches to CSV
        output_path = Path(output_csv)
        with output_path.open("w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["file", "key", "value"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matches)
        print(f"\nMatches saved to {output_csv}")


# Example usage
search_directory = "."  # Current directory
search_term = "3870948"
output_file = "matches.csv"
search_json_files(search_directory, search_term, output_file)
