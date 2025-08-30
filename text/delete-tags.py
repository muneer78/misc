import os
import re
import shutil


def modify_files_python(start_directory="."):
    """
    Finds files, backs them up, and modifies lines beginning with "tags:",
    containing another word, and the word "misc", by deleting "misc".

    Args:
        start_directory (str): The directory to start searching from.
    """
    target_regex = re.compile(r"^tags:[ \t]+.*\bmisc\b")
    # This regex is for identifying lines that match the criteria.
    # ^tags:        - Line starts with "tags:"
    # [ \t]+        - Followed by one or more spaces or tabs (ensures "another word")
    # .* - Any characters
    # \bmisc\b     - The whole word "misc" (using \b for word boundary)

    replacement_regex = re.compile(r"(\btags:[ \t]+.*)\bmisc\b")
    # This regex is for the actual replacement:
    # (tags:[ \t]+.*) - Capture group 1: "tags:", spaces/tabs, and everything before "misc"
    # \bmisc\b       - The word "misc" itself

    modified_files_count = 0

    print(f"Searching for files from directory: {start_directory}")

    for root, _, files in os.walk(start_directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Skip common binary/special files to prevent errors or unexpected behavior
            if not os.path.isfile(filepath) or os.path.islink(filepath):
                continue
            # Basic check to avoid binary files, not exhaustive but helpful
            if any(
                filepath.lower().endswith(ext)
                for ext in [
                    ".zip",
                    ".tar",
                    ".gz",
                    ".bz2",
                    ".rar",
                    ".7z",
                    ".exe",
                    ".dll",
                    ".so",
                    ".dylib",
                    ".pyc",
                    ".o",
                    ".a",
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".gif",
                    ".bmp",
                    ".mp3",
                    ".mp4",
                    ".avi",
                    ".mov",
                    ".pdf",
                    ".doc",
                    ".docx",
                    ".xls",
                    ".xlsx",
                    ".ppt",
                    ".pptx",
                ]
            ):
                # print(f"Skipping binary/archive file: {filepath}")
                continue

            try:
                # Read the file content
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Assume no modification until a match is found
                modified = False
                new_lines = []

                for line in lines:
                    if target_regex.search(line):
                        # Apply the replacement only if the line matches the criteria
                        new_line = replacement_regex.sub(r"\1", line)
                        if new_line != line:  # Check if substitution actually happened
                            new_lines.append(new_line)
                            modified = True
                        else:
                            new_lines.append(
                                line
                            )  # Append original if no actual change by sub
                    else:
                        new_lines.append(line)

                if modified:
                    # Create a backup
                    backup_filepath = filepath + ".bak"
                    shutil.copy2(filepath, backup_filepath)
                    print(f"Backed up: {filepath} to {backup_filepath}")

                    # Write the modified content back to the original file
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print(f"Modified file: {filepath}")
                    modified_files_count += 1

            except UnicodeDecodeError:
                print(f"Skipping file due to encoding error (not UTF-8): {filepath}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    print(f"\nProcessing complete. Total files modified: {modified_files_count}")


if __name__ == "__main__":
    # You can specify a different starting directory if needed
    # For example, to process files in the current directory:
    modify_files_python(".")
    # To process files in a specific folder:
    # modify_files_python("/path/to/your/folder")
