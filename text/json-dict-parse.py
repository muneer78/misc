import json
import csv
from pathlib import Path
from datetime import datetime as dt

current_date = dt.now().strftime("%Y%m%d%H%H")

# Specify the directory
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads")

# Output file
output_file = Path(
    rf"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\salesforce_responses_{current_date}.csv"
)

# Initialize a list to hold the data
data = []

# Iterate over all files in the directory
for file_path in directory.iterdir():
    if file_path.is_file() and file_path.suffix == ".json":
        with file_path.open("r", encoding="utf-8") as file:
            content = file.read().strip()

        # Split the content into individual JSON objects
        json_objects = content.split("\n")

        # Iterate over each JSON object
        for json_str in json_objects:
            json_str = json_str.strip()
            if json_str:
                # Convert the string to a Python dictionary or list
                try:
                    json_data = json.loads(json_str)
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error in file {file_path.name}: {e}")
                    continue

                # Handle case where json_data is a list
                if isinstance(json_data, list):
                    for item in json_data:
                        if isinstance(item.get("SalesforceResponse"), dict):
                            # Add the file name and Account__c to the item
                            item["SalesforceResponse"]["File"] = file_path.name
                            item["SalesforceResponse"]["Account"] = item.get(
                                "Account__c", ""
                            )

                            # Extract statusCode from SalesforceResponse errors
                            errors = item["SalesforceResponse"].get("errors", [])
                            if (
                                errors
                                and isinstance(errors, list)
                                and "statusCode" in errors[0]
                            ):
                                item["SalesforceResponse"]["statusCode"] = errors[0][
                                    "statusCode"
                                ]
                            else:
                                item["SalesforceResponse"]["statusCode"] = ""

                            # Add the SalesforceResponse to the data list
                            data.append(item["SalesforceResponse"])
                elif isinstance(json_data.get("SalesforceResponse"), dict):
                    # Add the file name and Account__c to the item
                    json_data["SalesforceResponse"]["File"] = file_path.name
                    json_data["SalesforceResponse"]["Account"] = json_data.get(
                        "Account__c", ""
                    )

                    # Extract statusCode from SalesforceResponse errors
                    errors = json_data["SalesforceResponse"].get("errors", [])
                    if (
                        errors
                        and isinstance(errors, list)
                        and "statusCode" in errors[0]
                    ):
                        json_data["SalesforceResponse"]["statusCode"] = errors[0][
                            "statusCode"
                        ]
                    else:
                        json_data["SalesforceResponse"]["statusCode"] = ""

                    # Add the SalesforceResponse to the data list
                    data.append(json_data["SalesforceResponse"])

# Write the data to a CSV file
if data:
    # Get the headers from the first item
    headers = data[0].keys()

    with output_file.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"Parsed data written to {output_file}")
else:
    print("No data found to write to CSV.")
