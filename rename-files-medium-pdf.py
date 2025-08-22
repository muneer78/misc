from pathlib import Path

# Specify the directory containing the files
directory = Path("/Users/muneer78/Downloads/convert")

# Iterate over all files in the directory
for file in directory.iterdir():
    if (
        file.is_file() and "-by" in file.stem
    ):  # Use `stem` to check the filename without extension
        # Separate the filename and extension
        name_part = file.stem[: file.stem.find("-by")].rstrip("-")
        extension = file.suffix
        # Construct the new filename
        new_name = f"{name_part}{extension}"
        new_path = file.with_name(new_name)
        # Rename the file
        file.rename(new_path)
        print(f"Renamed: {file.name} -> {new_name}")
