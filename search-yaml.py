import pathlib

def has_yaml_front_matter(lines):
    return lines and lines[0].strip() == "---"

def missing_title_or_date(lines):
    in_front_matter = False
    has_title = has_date = False
    for line in lines:
        if line.strip() == "---":
            if not in_front_matter:
                in_front_matter = True
                continue
            else:
                break  # End of front matter
        if in_front_matter:
            if line.lstrip().startswith("title:"):
                has_title = True
            if line.lstrip().startswith("date:"):
                has_date = True
    return in_front_matter and (not has_title or not has_date)

result = []
for path in pathlib.Path("/Users/muneer78/Documents/GitHub/reenum-blog/content/posts/writings").rglob("*"):
    if path.is_file():
        try:
            with path.open(encoding="utf-8") as f:
                lines = f.readlines()
            if has_yaml_front_matter(lines) and missing_title_or_date(lines):
                result.append(str(path))
        except Exception:
            continue

with open("missing_title_or_date.txt", "w", encoding="utf-8") as out:
    for item in result:
        print(item)
        out.write(item + "\n")