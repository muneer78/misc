import os
from PIL import Image

# Get the current working directory
current_directory = os.getcwd()

# List all files in the current directory
webp_files = [f for f in os.listdir(current_directory) if f.lower().endswith(".webp")]

# Convert each webp file to PNG
for webp_file in webp_files:
    webp_path = os.path.join(current_directory, webp_file)

    # Open the webp image
    im = Image.open(webp_path)

    # Create an output file path by changing the extension to PNG
    output_file = os.path.splitext(webp_file)[0] + ".png"
    png_path = os.path.join(current_directory, output_file)

    # Save the image as PNG
    im.save(png_path, "PNG")

print(f"Converted {len(webp_files)} webp files to PNG in {current_directory}")
