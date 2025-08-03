import pathlib

directory = "/Users/muneer78/Documents/GitHub/personal-site/content"

for path in pathlib.Path(directory).rglob("*"):
    if path.is_file():
        try:
            lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
            new_lines = [line for line in lines if line.strip() != "layout: post"]
            if len(new_lines) != len(lines):
                path.write_text("".join(new_lines), encoding="utf-8")
                print(f"Modified: {path}")
        except Exception:
            continue
print("Done.")