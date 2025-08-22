import pathlib

assets_dir = pathlib.Path(
    "/Users/muneer78/Documents/GitHub/personal-site/content/assets"
)
posts_dir = pathlib.Path("/Users/muneer78/Documents/GitHub/personal-site/content/posts")
output_file = pathlib.Path("/Users/muneer78/Downloads/image_references.txt")

image_names = {img.name for img in assets_dir.rglob("*") if img.is_file()}

results = []

for post_file in posts_dir.rglob("*"):
    if post_file.is_file():
        try:
            text = post_file.read_text(encoding="utf-8")
            for img_name in image_names:
                if img_name in text:
                    result = f"{img_name} found in {post_file}"
                    print(result)
                    results.append(result)
        except Exception:
            continue

results.sort()

with open(output_file, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")
