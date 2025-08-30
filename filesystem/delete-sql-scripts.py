from pathlib import Path


def delete_files_with_pattern(directory, pattern):
    directory_path = Path(directory)
    files_to_delete = directory_path.glob(
        pattern
    )  # Use glob method of Path to match the pattern
    for file in files_to_delete:
        file.unlink()  # Delete the file


if __name__ == "__main__":
    directory = r"C:\Users\mahmad\AppData\Roaming\DBeaverData\workspace6\General\Scripts"  # Specify the directory where files are located
    pattern = "Script-*.sql"  # Specify your pattern here
    delete_files_with_pattern(directory, pattern)
    print("Deletes are done")
