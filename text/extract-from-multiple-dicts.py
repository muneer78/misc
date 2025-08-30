import json
from pathlib import Path

# Specify the directory
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\archives\202501-dbx-qa-profiles")

# Output file
output_file = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\code\dbx-qa-nulls.txt")

# Initialize a list to hold the extracted records
all_records_with_nonzero_nulls = []

# Iterate over all files in the directory
for file_path in directory.iterdir():
    if file_path.is_file() and file_path.suffix == ".txt":
        with file_path.open("r", encoding="utf-8") as file:
            content = file.read().strip()

        # Convert the content to valid JSON format
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error in file {file_path.name}: {e}")
            continue

        # Extract records where count_null is not 0
        records_with_nonzero_nulls = {
            key: value for key, value in data.items() if value.get("count_null", 0) != 0
        }

        # Add the extracted records to the list
        all_records_with_nonzero_nulls.append(
            (file_path.name, records_with_nonzero_nulls)
        )

# Write the extracted records to the output file
with output_file.open("w", encoding="utf-8") as out_file:
    for file_name, records in all_records_with_nonzero_nulls:
        out_file.write(f"File: {file_name}\n")
        for key, value in records.items():
            out_file.write(f"Column: {key}\n")
            out_file.write(f"Total: {value['count']}\n")
            out_file.write(f"Non-null: {value['count_non_null']}\n")
            out_file.write(f"Null: {value['count_null']}\n")
            out_file.write("\n")
        out_file.write("---\n\n")

print(f"Extracted records written to {output_file}")
