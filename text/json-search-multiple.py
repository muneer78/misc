from pathlib import Path
import json


def search_json_files(directory, search_string):
    found_json = False  # Flag to track if any JSON files are found
    found_match = False  # Flag to track if any match is found

    # Convert the directory to a Path object
    directory_path = Path(directory)

    # Walk through the directory and subdirectories
    for file_path in directory_path.rglob("*.json"):  # Find all JSON files recursively
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
                                    print(
                                        f"Found '{search_string}' in '{key}' column of file: {file_path}"
                                    )
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
                                            print(
                                                f"Found '{search_string}' in '{key}' column of file: {file_path}"
                                            )
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


# Example usage
search_directory = "."  # Current directory
search_term = "3870948"
search_json_files(search_directory, search_term)
