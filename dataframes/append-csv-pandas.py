"""Append CSV files, with optional type normalization, de-duplication, and sorting."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append CSV files from explicit paths and/or directories."
    )
    parser.add_argument("files", nargs="*", type=Path, help="CSV files to append")
    parser.add_argument(
        "-d",
        "--directory",
        action="append",
        type=Path,
        default=[],
        help="Directory containing CSV files to append (may be repeated)",
    )
    parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Destination CSV file"
    )
    parser.add_argument(
        "--pattern", default="*.csv", help="Filename pattern for directory inputs"
    )
    parser.add_argument(
        "--preserve-types",
        action="store_true",
        help="Keep pandas-inferred column types instead of converting values to strings",
    )
    parser.add_argument(
        "--deduplicate", action="store_true", help="Drop duplicate rows after appending"
    )
    parser.add_argument("--sort-by", help="Column by which to sort the output")
    parser.add_argument(
        "--ascending", action="store_true", help="Sort ascending (the default is descending)"
    )
    return parser.parse_args()


def input_files(args: argparse.Namespace) -> list[Path]:
    files = list(args.files)
    for directory in args.directory:
        if not directory.is_dir():
            raise ValueError(f"Not a directory: {directory}")
        files.extend(directory.glob(args.pattern))

    output = args.output.resolve()
    return sorted({path.resolve() for path in files if path.resolve() != output})


def main() -> None:
    args = parse_args()
    files = input_files(args)
    if not files:
        raise SystemExit("Provide at least one CSV file or a directory containing CSV files.")

    frames = [pd.read_csv(file) for file in files]
    if not args.preserve_types:
        frames = [frame.astype(str) for frame in frames]

    combined = pd.concat(frames, ignore_index=True)
    initial_count = len(combined)

    if args.deduplicate:
        combined = combined.drop_duplicates()

    if args.sort_by:
        if args.sort_by not in combined.columns:
            raise ValueError(f"Sort column not found: {args.sort_by}")
        combined = combined.sort_values(args.sort_by, ascending=args.ascending)

    combined.to_csv(args.output, index=False)

    print(f"Appended {len(files)} CSV file(s).")
    print(f"Rows before de-duplication: {initial_count}")
    print(f"Rows written: {len(combined)}")
    if args.deduplicate:
        print(f"Duplicate rows removed: {initial_count - len(combined)}")
    print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()
