from pathlib import Path


def prepend_to_filenames(directory, prefix):
    # Loop through all files in the directory
    for file in Path(directory).iterdir():
        # Check if it is a file (not a directory)
        if file.is_file():
            # Create the new filename
            new_filename = prefix + file.name
            new_file_path = file.with_name(new_filename)

            # Rename the file
            file.rename(new_file_path)
            print(f"Renamed: {file.name} -> {new_filename}")


# Example usage
directory_path = "path/to/your/directory"  # Replace with your directory path
prefix_string = "polars-"  # Replace with your desired prefix
prepend_to_filenames(directory_path, prefix_string)
