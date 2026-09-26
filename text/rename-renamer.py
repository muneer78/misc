#!/usr/bin/env python3
"""Rename files from a two-column CSV mapping.

The command previews changes by default. Add ``--apply`` to rename files.

Examples:
    # CSV has OldName and NewName headers; paths are relative to this directory.
    python rename-renamer.py data.csv --source-dir books --apply

    # Headerless CSV; move matching files into a separate directory.
    python rename-renamer.py data.csv --no-header --source-dir books \
        --destination-dir books-renamed --apply
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_mappings(
    csv_path: Path, old_column: str, new_column: str, has_header: bool
) -> list[tuple[str, str]]:
    """Read nonblank old-name/new-name pairs from a mapping CSV."""
    with csv_path.open(newline="", encoding="utf-8-sig") as mapping_file:
        if has_header:
            reader = csv.DictReader(mapping_file)
            if not reader.fieldnames or old_column not in reader.fieldnames or new_column not in reader.fieldnames:
                available = ", ".join(reader.fieldnames or [])
                raise ValueError(
                    f"Expected columns {old_column!r} and {new_column!r}; found: {available}"
                )
            mappings = ((row[old_column], row[new_column]) for row in reader)
        else:
            reader = csv.reader(mapping_file)
            mappings = ((row[0], row[1]) for row in reader if len(row) >= 2)

        return [(old.strip(), new.strip()) for old, new in mappings if old.strip() and new.strip()]


def resolve_path(directory: Path, name: str) -> Path:
    """Resolve a mapping value as an absolute path or relative to ``directory``."""
    path = Path(name)
    return path if path.is_absolute() else directory / path


def rename_files(
    mappings: list[tuple[str, str]],
    source_dir: Path,
    destination_dir: Path,
    apply: bool,
    overwrite: bool,
) -> int:
    """Preview or apply mappings and return a nonzero status on failures."""
    failures = 0
    for old_name, new_name in mappings:
        source = resolve_path(source_dir, old_name)
        destination = resolve_path(destination_dir, new_name)

        if not source.exists():
            print(f"SKIP: source does not exist: {source}")
            failures += 1
            continue
        if destination.exists() and not overwrite:
            print(f"SKIP: destination already exists: {destination}")
            failures += 1
            continue

        action = "RENAME" if apply else "PREVIEW"
        print(f"{action}: {source} -> {destination}")
        if not apply:
            continue

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if overwrite:
                source.replace(destination)
            else:
                source.rename(destination)
        except OSError as error:
            print(f"WARNING: could not rename {source} to {destination}: {error}")
            failures += 1

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping_csv", type=Path, help="Two-column CSV containing old and new names")
    parser.add_argument("--source-dir", type=Path, default=Path("."), help="Directory containing source files")
    parser.add_argument(
        "--destination-dir",
        type=Path,
        help="Directory for renamed files (defaults to --source-dir)",
    )
    parser.add_argument("--old-column", default="OldName", help="Old-name header (default: OldName)")
    parser.add_argument("--new-column", default="NewName", help="New-name header (default: NewName)")
    parser.add_argument("--no-header", action="store_true", help="Treat the CSV as headerless")
    parser.add_argument("--apply", action="store_true", help="Perform the renames; otherwise only preview")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing destinations (requires --apply)")
    args = parser.parse_args()
    if args.overwrite and not args.apply:
        parser.error("--overwrite requires --apply")
    return args


def main() -> None:
    args = parse_args()
    mappings = read_mappings(
        args.mapping_csv, args.old_column, args.new_column, not args.no_header
    )
    destination_dir = args.destination_dir or args.source_dir
    failures = rename_files(
        mappings, args.source_dir, destination_dir, args.apply, args.overwrite
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
