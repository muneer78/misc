"""_summary_
Update files with specific prefix
"""

# from pathlib import Path
# import csv

# def count_records_in_csv_files(directory, filename_prefix):
#     total_record_count = 0
#     total_files_processed = 0

#     # Convert directory to Path object
#     directory_path = Path(directory)

#     # Iterate over all files in the directory
#     for file in directory_path.iterdir():
#         if file.is_file() and file.name.startswith(filename_prefix) and file.suffix.lower() == '.csv':
#             try:
#                 with file.open('r', newline='', encoding='utf-8') as f:
#                     reader = csv.reader(f)
#                     # Skip the header
#                     next(reader, None)
#                     # Count the remaining lines
#                     file_record_count = sum(1 for row in reader)
#                     total_record_count += file_record_count
#                     total_files_processed += 1
#                     print(f"Processed file: {file.name}, Records: {file_record_count}")
#             except Exception as e:
#                 print(f"Error processing file {file.name}: {e}")

#     return total_record_count, total_files_processed

# # Example usage
# directory = r'C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\checks'  # Current directory
# filename_prefix = 'cadence'
# total_records, files_processed = count_records_in_csv_files(directory, filename_prefix)
# print(f'Total number of records (excluding headers): {total_records}')
# print(f'Total number of files processed: {files_processed}')

# single file
# Example usage
directory = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\checks"  # Current directory
filename_prefix = "cadence"
total_records, files_processed = count_records_in_csv_files(directory, filename_prefix)
print(f"Total number of records (excluding headers): {total_records}")
print(f"Total number of files processed: {files_processed}")

from pathlib import Path
import csv


def count_records_in_csv_files(directory):
    total_record_count = 0
    total_files_processed = 0

    # Convert directory to Path object
    directory_path = Path(directory)

    # Iterate over all CSV files in the directory
    for file in directory_path.iterdir():
        if file.suffix.lower() == ".csv" and file.is_file():
            try:
                with file.open("r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    # Skip the header
                    next(reader, None)
                    # Count the remaining lines
                    file_record_count = sum(1 for row in reader)
                    total_record_count += file_record_count
                    total_files_processed += 1
                    print(f"Processed file: {file.name}, Records: {file_record_count}")
            except Exception as e:
                print(f"Error processing file {file.name}: {e}")

    return total_record_count, total_files_processed


# Example usage
directory = r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads\checks"  # Current directory
total_records, files_processed = count_records_in_csv_files(directory)
print(f"Total number of records (excluding headers): {total_records}")
print(f"Total number of files processed: {files_processed}")
