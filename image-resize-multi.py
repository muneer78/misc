import os
from PIL import Image

# String to search for in filenames
search_string = "Hyundai"

# Resize factor
resize_factor = 0.75

# Get current directory
current_directory = os.getcwd()

# Loop through all files in the current directory
for filename in os.listdir(current_directory):
    if search_string in filename and (
        filename.endswith(".jpg") or filename.endswith(".png")
    ):
        try:
            # Open image
            with Image.open(filename) as img:
                # Calculate new size
                new_size = (
                    int(img.width * resize_factor),
                    int(img.height * resize_factor),
                )

                # Resize image
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

                # Save resized image, overwrite the original
                resized_img.save(filename)
                print(f"Resized image saved: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
