from PIL import Image
from pathlib import Path


def resize_image_to_target_size(
    input_path, output_path, target_size_kb, step=5, quality_start=95
):
    """
    Resize an image to a specific file size by adjusting its quality.

    :param input_path: Path to the input image.
    :param output_path: Path to save the resized image.
    :param target_size_kb: Target file size in kilobytes.
    :param step: Step to decrease quality for each iteration.
    :param quality_start: Starting quality value (1-100).
    """
    target_size_bytes = target_size_kb * 1024
    quality = quality_start

    input_path = Path(input_path)
    output_path = Path(output_path)

    with Image.open(input_path) as img:
        # Ensure RGB mode for compatibility
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        while quality > 0:
            # Save the image with the current quality setting
            img.save(output_path, "JPEG", quality=quality)

            # Check the file size
            current_size = output_path.stat().st_size

            if current_size <= target_size_bytes:
                print(
                    f"Success: Image resized to {current_size / 1024:.2f} KB with quality {quality}."
                )
                return

            # Reduce the quality
            quality -= step

        print("Warning: Could not achieve the target file size.")


if __name__ == "__main__":
    # Example usage
    input_image_path = "/Users/muneer78/Downloads/IMG_1276.png"
    output_image_path = "/Users/muneer78/Downloads/IMG_1276-reduced.png"
    target_file_size_kb = 2000  # Target file size in KB

    resize_image_to_target_size(
        input_image_path, output_image_path, target_file_size_kb
    )
