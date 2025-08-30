import json


def count_records_in_json(file_path):
    record_count = 0
    skipped_count = 0

    try:
        # Open the file and read line by line
        with open(file_path, "r") as file:
            for line in file:
                try:
                    # Attempt to parse each line as JSON
                    record = json.loads(line)
                    if isinstance(record, list):
                        record_count += len(record)
                    elif isinstance(record, dict):
                        record_count += 1
                except json.JSONDecodeError:
                    # Increment the skip count for invalid JSON lines
                    skipped_count += 1

        return record_count, skipped_count

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return 0, 0  # Return 0 for both counts if there was an error


# Load the JSON file
file_path = "pipeline_errors2.json"
record_count = count_records_in_json(file_path)
print(f"Total number of records: {record_count}")
