def format_text_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()


formatted_lines = [line.strip() for line in lines if line.strip()]

with open(file_path, "w") as file:
    file.write("\n".join(formatted_lines))
# Usage
format_text_file("large_text_file.txt")
