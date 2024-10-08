from PIL import Image, ImageOps

def combine_images_vertically(image_paths, output_path, border_size=10, border_color=(0, 0, 0)):
    # Open all images, add borders, and calculate the total height and maximum width
    images = [ImageOps.expand(Image.open(img), border=border_size, fill=border_color) for img in image_paths]
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)

    # Create a new blank image with the calculated dimensions
    combined_image = Image.new("RGB", (max_width, total_height))

    # Paste each image into the combined image
    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    # Save the combined image
    combined_image.save(output_path)

# Example usage
image_files = ["oldmen1.jpg", "oldmen2.jpg", "oldmen3.jpg", "oldmen4.jpg", "oldmen5.jpg", "oldmen6.jpg", "oldmen7.jpg"]
combine_images_vertically(image_files, "oldmen.jpg", border_size=10, border_color=(0, 0, 0))
