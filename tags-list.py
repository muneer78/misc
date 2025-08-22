import os
import csv
import re
from collections import Counter

POSTS_DIR = "content"  # Adjust if your posts are elsewhere
OUTPUT_CSV = "tags-count.csv"


def extract_tags_from_file(filepath):
    tags = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().lower().startswith("tags:"):
                # Example: tags: python, fastapi, web
                tag_line = line.split(":", 1)[1]
                tags = [t.strip() for t in re.split(r"[,\s]+", tag_line) if t.strip()]
                break
    return tags


def main():
    tag_counter = Counter()
    for root, _, files in os.walk(POSTS_DIR):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                tags = extract_tags_from_file(filepath)
                tag_counter.update(tags)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["tag", "count"])
        for tag, count in sorted(tag_counter.items()):
            writer.writerow([tag, count])
    print(f"Tag counts written to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
