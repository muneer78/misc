from pathlib import Path
import re

# Directory containing the files
content_dir = Path.cwd() / "content"

# Pattern: line starts (possibly with spaces) with "tag: tags:"
pattern = re.compile(r"^\s*tag:\s*tags:\s*", re.IGNORECASE)

# Loop through files
for file_path in content_dir.iterdir():
    if not file_path.is_file() or file_path.name == ".DS_Store":
        continue

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
        updated_lines = []
        updated = False

        for line in lines:
            if pattern.match(line):
                updated_lines.append("tags:\n")
                updated = True
            else:
                updated_lines.append(line)

        if updated:
            file_path.write_text("".join(updated_lines), encoding="utf-8")
            print(f"✅ Cleaned tag: tags: → tags: in {file_path.name}")

    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")
