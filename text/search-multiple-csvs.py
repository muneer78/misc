from pathlib import Path
import csv


def search_csv_files(directory, search_string):
    # Get a list of all CSV files in the directory
    files = list(directory.glob("*.csv"))

    # Iterate through each CSV file
    for file_path in files:
        print(f"Searching in file: {file_path.name}")

        # Open the CSV file
        with file_path.open("r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

            # Iterate through each row in the CSV file
            for line_number, row in enumerate(reader, start=1):
                # Check if the search string is in any column
                if any(search_string.lower() in column.lower() for column in row):
                    print(
                        f"Found in file: {file_path.name}, line: {line_number}, row: {row}"
                    )
    else:
        print("Not found")


# Define the directory containing the CSV files
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\code\csv_files")

# Define the search string
search_string = "example"

# Call the function to search CSV files
search_csv_files(directory, search_string)
