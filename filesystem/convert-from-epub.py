from pathlib import Path
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup


def epub_to_text(epub_path, txt_path):
    book = epub.read_epub(epub_path)
    text = []

    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), "html.parser")
            text.append(soup.get_text())

    with txt_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(text))


def convert_folder(epub_folder, txt_folder):
    epub_folder = Path(epub_folder)
    txt_folder = Path(txt_folder)

    if not txt_folder.exists():
        txt_folder.mkdir(parents=True)

    for epub_file in epub_folder.glob("*.epub"):
        txt_file = txt_folder / f"{epub_file.stem}.txt"
        epub_to_text(epub_file, txt_file)
        print(f"Converted {epub_file} to {txt_file}")


# Example usage
epub_folder = "/Users/muneer78/Downloads/convert"
txt_folder = "/Users/muneer78/Downloads/docs"
convert_folder(epub_folder, txt_folder)
