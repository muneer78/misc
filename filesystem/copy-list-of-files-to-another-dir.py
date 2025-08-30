import os
import csv
import shutil


def copy_files_based_on_csv(csv_file, source_dir, dest_dir):
    """Copies files from source_dir to dest_dir based on filenames in csv_file.

    Args:
      csv_file: Path to the CSV file containing filenames.
      source_dir: Path to the source directory.
      dest_dir: Path to the destination directory.
    """

    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    with open(csv_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            filename = row[0]  # Assuming filename is in the first column
            source_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(dest_dir, filename)
            if os.path.exists(source_file):
                shutil.copy2(source_file, dest_file)


# Example usage:
csv_file_path = "/Users/muneer78/PycharmProjects/misc/missing_titles.csv"
source_directory = "/Users/muneer78/quartz/content/"
destination_directory = "/Users/muneer78/Desktop/saved/"
copy_files_based_on_csv(csv_file_path, source_directory, destination_directory)
