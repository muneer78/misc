from pathlib import Path
from PIL import Image
import pytesseract
from tqdm import tqdm

download_folder = Path('/Users/muneer78/pics/chuck_lorre_images')

# Iterate through the folder and extract text from all images
with open('lorre.md', 'a') as md_file:
    for image_file in tqdm(sorted(download_folder.iterdir()), desc="Processing images"):
        if image_file.suffix.lower() in {'.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'}:
            text = pytesseract.image_to_string(Image.open(image_file))
            md_file.write(text)
            md_file.write('\n---\n')

print("Finished scraping all pages and extracting text from images.")