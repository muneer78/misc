import csv
from pathlib import Path


def process_md_files_pathlib(root_folder: Path, output_csv_file: Path):
    """
    Recursively searches a folder for Markdown files, extracts the "tags" line,
    and saves the file path, name, and tags line to a CSV file.

    Args:
        root_folder (Path): The path to the folder to start searching from (Path object).
        output_csv_file (Path): The path to the output CSV file (Path object).
    """
    with open(output_csv_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Path", "File Name", "Tags Line"])  # Write header

        for filepath in root_folder.rglob("*.md"):
            tags_line = ""
            try:
                # Open the file and search for the tags line
                with open(filepath, "r", encoding="utf-8") as md_file:
                    for line in md_file:
                        if line.strip().lower().startswith("tags:"):
                            tags_line = line.strip()
                            break  # Found the tags line, no need to read further

                # Write to CSV
                csv_writer.writerow([str(filepath), filepath.name, tags_line])
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")


if __name__ == "__main__":
    # --- Configuration ---
    # Replace 'your_folder_path_here' with the actual path to your folder
    # Use Path() to create a Path object
    folder_to_scan = Path("/Users/muneer78/Documents/GitHub/mun-ssg/content")
    csv_output_name = Path(
        "/Users/muneer78/Documents/GitHub/mun-ssg/md_file_tags_pathlib.csv"
    )
    # -------------------

    if not folder_to_scan.is_dir():
        print(
            f"Error: The specified folder '{folder_to_scan}' does not exist or is not a directory."
        )
    else:
        print(f"Scanning '{folder_to_scan}' for Markdown files using pathlib...")
        process_md_files_pathlib(folder_to_scan, csv_output_name)
        print(f"Processing complete. Results saved to '{csv_output_name}'.")
