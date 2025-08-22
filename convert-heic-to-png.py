from PIL import Image  # Correct import for PIL
from pathlib import Path
from pillow_heif import register_heif_opener
from tqdm import tqdm
from argparse import ArgumentParser

register_heif_opener()


def main(params):
    print("Converting HEIC files to PNG")
    files = list(Path(".").glob("*.heic")) + list(Path(".").glob("*.HEIC"))

    if len(files) == 0:
        print("No HEIC files found")
        return

    for f in tqdm(files):
        try:
            image = Image.open(str(f))
            image.convert("RGB").save(str(f.with_suffix(".png")))
            if params.delete:
                f.unlink()  # Deletes the original HEIC file if delete flag is set
        except Exception as e:
            print(f"Error processing file {f}: {e}")


if __name__ == "__main__":
    parser = ArgumentParser()
    # delete option, default is False
    parser.add_argument(
        "-d", "--delete", action="store_true", help="Delete the file after conversion"
    )
    params = parser.parse_args()
    main(params)
