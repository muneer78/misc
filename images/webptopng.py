from PIL import Image
from pathlib import Path

# Get the current working directory
current_directory = Path("/Users/muneer78/Downloads/convert-images")

# List all .webp files in the current directory
webp_files = list(current_directory.glob("*.webp"))

# Convert each webp file to PNG
for webp_file in webp_files:
    # Open the webp image
    im = Image.open(webp_file)

    # Create an output file path by changing the extension to PNG
    png_path = webp_file.with_suffix(".png")

    # Save the image as PNG
    im.save(png_path, "PNG")

print(f"Converted {len(webp_files)} webp files to PNG in {current_directory}")
