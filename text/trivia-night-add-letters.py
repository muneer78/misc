from pathlib import Path

file_path = Path("/Users/muneer78/Documents/Projects/trivia-night/2025-02-03.md")

with file_path.open("r", encoding="utf-8") as file:
    lines = file.readlines()

updated_lines = []
i = 0
while i < len(lines):
    if lines[i].strip():  # Skip blank lines
        updated_lines.append(lines[i])
        if lines[i].strip().endswith("?"):
            if i + 1 < len(lines) and lines[i + 1].strip():
                updated_lines.append("A. " + lines[i + 1].strip() + "\n")
            if i + 2 < len(lines) and lines[i + 2].strip():
                updated_lines.append("B. " + lines[i + 2].strip() + "\n")
            if i + 3 < len(lines) and lines[i + 3].strip():
                updated_lines.append("C. " + lines[i + 3].strip() + "\n")
            if i + 4 < len(lines) and lines[i + 4].strip():
                updated_lines.append("D. " + lines[i + 4].strip() + "\n")
            i += 4
    i += 1

with file_path.open("w", encoding="utf-8") as file:
    file.writelines(updated_lines)

print("File has been updated.")
