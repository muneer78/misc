# import json
# import csv
# import polars as pl

# filtered_data = []

# # Read the JSON file line by line with the correct encoding
# with open("carrier_profile_20240506135435879946.json", "r", encoding="utf-8") as file:
#     for line in file:
#         try:
#             entry = json.loads(line)
#             # Filter out undesired patterns
#             if "salesforce_response_metrics" in entry or "input_file" in entry:
#                 continue

#             # Flatten SalesforceResponse into the main dictionary
#             salesforce_response = entry.pop("SalesforceResponse", {})
#             for key, value in salesforce_response.items():
#                 entry[f"SalesforceResponse_{key}"] = value

#             filtered_data.append(entry)
#         except json.JSONDecodeError as e:
#             print(f"Skipping invalid JSON entry: {e}")

# # Define the CSV file name
# csv_file = "extracted_data.csv"

# # Write the filtered data to a CSV file
# if filtered_data:
#     # Extract field names from the first entry
#     fieldnames = filtered_data[0].keys()

#     with open(csv_file, "w", newline="", encoding="utf-8") as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in filtered_data:
#             writer.writerow(row)

#     print(f"Data has been processed and saved as CSV. Check the file {csv_file}")
# else:
#     print("No valid data to write to CSV.")

# # Read the CSV with Polars, specifying dtypes and handling errors
# try:
#     df = pl.read_csv("extracted_data.csv", infer_schema_length=10000)
# except pl.exceptions.ComputeError as e:
#     print(f"Error reading CSV: {e}")
#     with open(csv_file, "r", encoding="utf-8", errors="replace") as file:
#         lines = file.readlines()

#     with open(csv_file, "w", encoding="utf-8") as file:
#         for line in lines:
#             file.write(line.encode("utf-8", errors="ignore").decode("utf-8"))

#     df = pl.read_csv("extracted_data.csv", infer_schema_length=10000)

# # Filter the DataFrame
# results_df = df.filter(pl.col("SalesforceResponse_success") == 'false')

# # Write the filtered data to another CSV file
# results_df.write_csv("finalerrorfile.csv")
# print("Error only CSV file created")

# # use this for multiple files
import os
import json
import csv
import polars as pl


def process_json_files(directory):
    # List all JSON files in the directory
    input_files = [f for f in os.listdir(directory) if f.endswith(".json")]

    for i, input_file in enumerate(input_files, start=1):
        filtered_data = []

        # Read the JSON file line by line with the correct encoding
        with open(os.path.join(directory, input_file), "r", encoding="utf-8") as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    # Filter out undesired patterns
                    if "salesforce_response_metrics" in entry or "input_file" in entry:
                        continue

                    # Flatten SalesforceResponse into the main dictionary
                    salesforce_response = entry.pop("SalesforceResponse", {})
                    for key, value in salesforce_response.items():
                        entry[f"SalesforceResponse_{key}"] = value

                    filtered_data.append(entry)
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON entry in {input_file}: {e}")

        # Define the CSV file name using f-string for numbering
        csv_file = os.path.join(directory, f"extracted_data_{i}.csv")

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

        # Read the CSV with Polars, specifying dtypes and handling errors
        try:
            df = pl.read_csv(csv_file, infer_schema_length=10000)
        except pl.exceptions.ComputeError as e:
            print(f"Error reading CSV {csv_file}: {e}")
            with open(csv_file, "r", encoding="utf-8", errors="replace") as file:
                lines = file.readlines()

            with open(csv_file, "w", encoding="utf-8") as file:
                for line in lines:
                    file.write(line.encode("utf-8", errors="ignore").decode("utf-8"))

            df = pl.read_csv(csv_file, infer_schema_length=10000)

        # Filter the DataFrame
        results_df = df.filter(pl.col("SalesforceResponse_success") == "false")

        # Write the filtered data to another CSV file using f-string for numbering
        error_csv_file = os.path.join(directory, f"finalerrorfile_{i}.csv")
        results_df.write_csv(error_csv_file)
        print(f"Error-only CSV file created for {input_file} as {error_csv_file}")


# Example usage
directory_path = "."  # Replace with the path to your JSON files directory
process_json_files(directory_path)
