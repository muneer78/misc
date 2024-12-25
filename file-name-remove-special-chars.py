from pathlib import Path

# Specify the directory containing the files
# directory = Path("/Users/muneer78/reading/documents")
directory = Path("/Users/muneer78/Downloads/convert")

# Characters to remove
chars_to_remove = "'`()_|#?%\/,&"

# Iterate over all files in the directory
for file in directory.iterdir():
    if file.is_file():
        # Remove specified characters from the filename (stem + extension)
        cleaned_name = ''.join(char for char in file.name if char not in chars_to_remove)
        new_path = file.with_name(cleaned_name)
        # Rename the file
        file.rename(new_path)
        print(f"Renamed: {file.name} -> {cleaned_name}")
