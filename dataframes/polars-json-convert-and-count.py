import json
from datetime import datetime
from collections import defaultdict
import polars as pl


def count_records_in_json(file_path):
    record_count = 0
    skipped_count = 0
    date_count = defaultdict(int)

    try:
        # Open the file and read line by line
        with open(file_path, "r") as file:
            for line in file:
                try:
                    # Attempt to parse each line as JSON
                    record = json.loads(line)

                    # Check if it's a dictionary and has the 'timestamp' key
                    if isinstance(record, dict) and "timestamp" in record:
                        # Convert timestamp to date
                        timestamp = record["timestamp"]
                        date = datetime.utcfromtimestamp(timestamp / 1000).strftime(
                            "%Y-%m-%d"
                        )

                        # Increment the count for this date
                        date_count[date] += 1
                        record_count += 1
                    elif isinstance(record, list):
                        for item in record:
                            if "timestamp" in item:
                                timestamp = item["timestamp"]
                                date = datetime.utcfromtimestamp(
                                    timestamp / 1000
                                ).strftime("%Y-%m-%d")
                                date_count[date] += 1
                                record_count += 1
                            else:
                                skipped_count += 1
                    else:
                        skipped_count += 1
                except json.JSONDecodeError:
                    # Increment the skip count for invalid JSON lines
                    skipped_count += 1

        return record_count, skipped_count, date_count

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return (
        0,
        0,
        {},
    )  # Return 0 for both counts and an empty dictionary if there was an error


# Load the JSON file
file_path = "pipeline_errors2.json"
record_count, skipped_count, date_count = count_records_in_json(file_path)
print(f"Total number of records: {record_count}")
print(f"Number of skipped records: {skipped_count}")

# Convert the date_count dictionary to a Polars DataFrame
date_df = pl.DataFrame(
    {"date": list(date_count.keys()), "count": list(date_count.values())}
)
print(date_df)
