import os
import shutil


def restore_and_delete_backups(start_directory="."):
    """
    Restores original files from .bak backups and deletes the current modified files.

    Args:
        start_directory (str): The directory to start searching from.
    """
    restored_count = 0
    deleted_count = 0

    print(f"Searching for .bak files from directory: {start_directory}")

    for root, _, files in os.walk(start_directory):
        for filename in files:
            if filename.endswith(".bak"):
                backup_filepath = os.path.join(root, filename)
                original_filepath = backup_filepath[:-4]  # Remove the '.bak' extension

                print(f"Found backup: {backup_filepath}")

                try:
                    # 1. Restore the original file from the .bak
                    if os.path.exists(original_filepath):
                        # If the original file exists, delete it first before moving the backup
                        os.remove(original_filepath)
                        print(f"Deleted current file: {original_filepath}")
                        deleted_count += 1

                    shutil.move(backup_filepath, original_filepath)
                    print(f"Restored: {backup_filepath} to {original_filepath}")
                    restored_count += 1

                except Exception as e:
                    print(f"Error restoring {backup_filepath}: {e}")

    print(f"\nRestoration complete.")
    print(f"Total files restored from backup: {restored_count}")
    print(f"Total current files deleted (replaced by backup): {deleted_count}")


if __name__ == "__main__":
    # Specify the directory where you want to restore files
    # For example, to restore files in the current directory and its subdirectories:
    restore_and_delete_backups(".")
    # To restore files in a specific folder:
    # restore_and_delete_backups("/path/to/your/folder")