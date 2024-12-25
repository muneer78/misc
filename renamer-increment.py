import os
from collections import defaultdict

def rename_files(directory, id, start_record):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Initialize the record number dictionary
    record_numbers = defaultdict(lambda: start_record - 1)
    
    # Loop through each file in the directory
    for filename in files:
        # Get the file extension
        _, file_extension = os.path.splitext(filename)
        
        # Construct the new filename prefix
        new_filename_prefix = f"{id}"
        
        # Increment the record number for the prefix
        record_numbers[new_filename_prefix] += 1
        new_filename = f"{new_filename_prefix}-{record_numbers[new_filename_prefix]}"
        
        # Add the file extension to the new filename
        new_filename_with_extension = f"{new_filename}{file_extension}"
        
        # Construct full file paths
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename_with_extension)
        
        try:
            # Rename the file
            os.rename(old_file, new_file)
            print(f"Renamed '{filename}' to '{new_filename_with_extension}'")
        except Exception as e:
            print(f"Error renaming file '{filename}': {e}")

    print("Files have been renamed successfully.")

# Static directory path
directory = r"C:\Users\mahmad\OneDrive - Ryan RTS\1-Projects\Python\rename"

# Input the id and starting record number
id = input("Enter the ID: ")
start_record = int(input("Enter the starting record number: "))

# Call the function to rename files
rename_files(directory, id, start_record)
