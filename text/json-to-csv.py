import os
import json
import csv
from pathlib import Path


def process_json_files(directory):
    # List all JSON files in the directory
    input_files = [f for f in os.listdir(directory) if f.endswith(".json")]

    for input_file in input_files:
        filtered_data = []

        # Read the JSON file with the correct encoding
        with open(os.path.join(directory, input_file), "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):
                    filtered_data.extend(data)
                else:
                    filtered_data.append(data)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON file {input_file}: {e}")
                continue

        # Define the CSV file name using the original JSON filename
        csv_file = os.path.join(directory, f"{Path(input_file).stem}_extracted.csv")

        # Write the filtered data to a CSV file
        if filtered_data:
            # Extract field names from the first entry
            fieldnames = filtered_data[0].keys()

            with open(csv_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in filtered_data:
                    writer.writerow(row)

            print(
                f"Data from {input_file} has been processed and saved as CSV: {csv_file}"
            )
        else:
            print(f"No valid data to write to CSV for file {input_file}.")


# Example usage
directory_path = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\csv"  # Replace with the path to your JSON files directory
process_json_files(directory_path)
