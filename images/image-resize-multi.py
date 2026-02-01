import os
from PIL import Image

# Set the directory to process images in
directory = '/Users/muneer78/Downloads'  # Change this as needed

# String to search for in filenames
search_string = "bonfire"

# Resize factor
resize_factor = 0.25

for filename in os.listdir(directory):
    if search_string in filename and (
        filename.endswith(".jpg") or filename.endswith(".png")
    ):
        try:
            file_path = os.path.join(directory, filename)
            with Image.open(file_path) as img:
                new_size = (
                    int(img.width * resize_factor),
                    int(img.height * resize_factor),
                )
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                resized_img.save(file_path)
                print(f"Resized image saved: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")