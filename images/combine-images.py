#!/usr/bin/env python3

import argparse
from pathlib import Path

from PIL import Image, ImageColor, ImageOps


def combine_images(
    first_path: Path,
    second_path: Path,
    output_path: Path,
    direction: str = "horizontal",
    spacing: int = 0,
    background: str = "white",
) -> None:
    color = ImageColor.getrgb(background)

    with Image.open(first_path) as first_source, Image.open(second_path) as second_source:
        first = ImageOps.exif_transpose(first_source).convert("RGBA")
        second = ImageOps.exif_transpose(second_source).convert("RGBA")

        if direction == "horizontal":
            size = (first.width + second.width + spacing, max(first.height, second.height))
            first_position = (0, (size[1] - first.height) // 2)
            second_position = (first.width + spacing, (size[1] - second.height) // 2)
        else:
            size = (max(first.width, second.width), first.height + second.height + spacing)
            first_position = ((size[0] - first.width) // 2, 0)
            second_position = ((size[0] - second.width) // 2, first.height + spacing)

        combined = Image.new("RGBA", size, (*color, 255))
        combined.alpha_composite(first, first_position)
        combined.alpha_composite(second, second_position)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.suffix.lower() in {".jpg", ".jpeg"}:
            combined.convert("RGB").save(output_path)
        else:
            combined.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Combine two images into one image.")
    parser.add_argument("first", type=Path, help="path to the first image")
    parser.add_argument("second", type=Path, help="path to the second image")
    parser.add_argument("output", type=Path, help="path for the combined image")
    parser.add_argument(
        "--direction",
        choices=("horizontal", "vertical"),
        default="horizontal",
        help="how to arrange the images (default: horizontal)",
    )
    parser.add_argument(
        "--spacing",
        type=int,
        default=0,
        help="pixels between the images (default: 0)",
    )
    parser.add_argument(
        "--background",
        default="white",
        help="background color name or hex value (default: white)",
    )
    args = parser.parse_args()

    if args.spacing < 0:
        parser.error("--spacing must be zero or greater")

    try:
        combine_images(
            args.first,
            args.second,
            args.output,
            args.direction,
            args.spacing,
            args.background,
        )
    except (FileNotFoundError, Image.UnidentifiedImageError, ValueError, OSError) as error:
        parser.error(str(error))

    print(f"Combined image saved to {args.output}")


if __name__ == "__main__":
    main()
