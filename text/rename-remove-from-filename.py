from pathlib import Path

# Define the directory to process
directory = Path(r"C:\Users\mahmad\OneDrive - Ryan RTS\code\update")

# Ensure the directory exists
if directory.is_dir():
    for file in directory.iterdir():
        if file.is_file():  # Only process files
            # Remove the string 'updated' from the file name
            new_name = file.name.replace("5185", "5951")
            new_name = new_name.strip()  # Remove leading/trailing whitespace

            # Rename the file if the name has changed
            if new_name != file.name:
                new_path = file.with_name(new_name)
                file.rename(new_path)
                print(f"Renamed: {file.name} -> {new_name}")
else:
    print(f"Directory does not exist: {directory}")
