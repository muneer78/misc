import csv
import os

def rename_files(csv_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script file
    # directory = script_dir  # Use the script's directory as the target directory
    directory = '/Users/muneer78/Downloads/rename'  # Use the script's directory as the target directory

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            current_name = row[0]
            new_name = row[1] + ".epub"  # Append .epub extension
            current_path = os.path.join(directory, current_name)
            new_path = os.path.join(directory, new_name)
            
            try:
                os.rename(current_path, new_path)
                print(f"Renamed {current_name} to {new_name}")
            except FileNotFoundError:
                print(f"File {current_name} not found")
            except FileExistsError:
                print(f"File {new_name} already exists")

# Usage example
csv_file_path = '/Users/muneer78/Downloads/renamed_files_filenames_only.csv'

rename_files(csv_file_path)