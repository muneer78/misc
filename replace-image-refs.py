import pathlib

search = "https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/"
replace = "../../assets/"

for path in pathlib.Path("/Users/muneer78/Documents/GitHub/personal-site").rglob("*"):
    if path.is_file():
        try:
            text = path.read_text(encoding="utf-8")
            if search in text:
                new_text = text.replace(search, replace)
                path.write_text(new_text, encoding="utf-8")
        except Exception:
            continue
