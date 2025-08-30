# import os
# import csv
# import re


# def search_csv_files(directory, output_file):
#     # Regular expression to match numbers with more than two digits after the decimal point
#     pattern = re.compile(r"\d+\.\d{3,}")
#     results = []

#     # Get a list of all files in the directory
#     files = [file for file in os.listdir(directory) if file.endswith(".csv")]

#     # Iterate through each CSV file
#     for file_name in files:
#         file_path = os.path.join(directory, file_name)
#         print(f"Searching in file: {file_name}")

#         # Open the CSV file
#         with open(file_path, "r", newline="") as csvfile:
#             reader = csv.reader(csvfile)

#             # Iterate through each row in the CSV file
#             for row in reader:
#                 # Check each column for the pattern
#                 for column in row:
#                     if pattern.search(column):
#                         results.append([file_name] + row)
#                         break

#     # Write results to a new CSV file
#     with open(output_file, "w", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["File Name", "Row Data"])
#         writer.writerows(results)


# # Define the directory containing the CSV files
# directory = r"c:\Users\mahmad\OneDrive - Ryan RTS\Downloads"

# # Define the output file
# output_file = "search_results.csv"

# # Call the function to search CSV files and write results
# search_csv_files(directory, output_file)

#
import os
import csv
import re


def search_csv_files(directory, output_file):
    # Regular expression to match numbers with more than two digits after the decimal point
    pattern = re.compile(r"\d+\.\d{3,}")
    results = []

    # Get a list of all files in the directory
    files = [file for file in os.listdir(directory) if file.endswith(".csv")]

    # Iterate through each CSV file
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        print(f"Searching in file: {file_name}")

        # Open the CSV file
        with open(file_path, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)

            # Iterate through each row in the CSV file
            for row in reader:
                # Check each column for the pattern
                for column in row:
                    if pattern.search(column):
                        results.append([file_name] + row)
                        break

    # Write results to a new CSV file
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "Row Data"])
        writer.writerows(results)


# Define the directory containing the CSV files
directory = r"c:\Users\mahmad\OneDrive - Ryan RTS\Downloads"

# Define the output file
output_file = "search_results2.csv"

# Call the function to search CSV files and write results
search_csv_files(directory, output_file)
