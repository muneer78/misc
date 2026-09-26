"""Compare CSV datasets row by row or produce a source-labelled combined file."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_labelled_file(value: str) -> tuple[str, Path]:
    try:
        label, filename = value.split("=", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use LABEL=FILE.csv") from error
    if not label or not filename:
        raise argparse.ArgumentTypeError("Use LABEL=FILE.csv")
    return label, Path(filename)


def parse_pair(value: str) -> tuple[str, Path, Path]:
    try:
        label, filenames = value.split("=", 1)
        left, right = filenames.split(",", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use LABEL=NEW.csv,OLD.csv") from error
    if not label or not left or not right:
        raise argparse.ArgumentTypeError("Use LABEL=NEW.csv,OLD.csv")
    return label, Path(left), Path(right)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare sorted CSVs or combine CSVs with a source column."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    differences = subparsers.add_parser(
        "differences", help="Write changed rows from one or more CSV pairs"
    )
    differences.add_argument(
        "--pair",
        action="append",
        required=True,
        type=parse_pair,
        metavar="LABEL=NEW.csv,OLD.csv",
        help="Named pair to compare; may be repeated",
    )
    differences.add_argument("--key", required=True, help="Column used to sort both files")
    differences.add_argument("-o", "--output", type=Path, required=True)

    sources = subparsers.add_parser(
        "sources", help="Combine named CSVs and add a source column"
    )
    sources.add_argument(
        "--input",
        action="append",
        required=True,
        type=parse_labelled_file,
        metavar="LABEL=FILE.csv",
        help="Named CSV file; may be repeated",
    )
    sources.add_argument("--key", required=True, help="Column used to sort the result")
    sources.add_argument("--source-column", default="Source")
    sources.add_argument("-o", "--output", type=Path, required=True)
    return parser.parse_args()


def read_sorted(filename: Path, key: str) -> pd.DataFrame:
    frame = pd.read_csv(filename)
    if key not in frame.columns:
        raise ValueError(f"Key column {key!r} is missing from {filename}")
    return frame.sort_values(key).reset_index(drop=True)


def differing_rows(new: pd.DataFrame, old: pd.DataFrame) -> pd.DataFrame:
    """Return rows from *new* that differ from the aligned *old* file."""
    columns = new.columns.union(old.columns, sort=False)
    new, old = new.reindex(columns=columns), old.reindex(columns=columns)
    size = max(len(new), len(old))
    new, old = new.reindex(range(size)), old.reindex(range(size))
    return new.loc[new.ne(old).any(axis=1)].dropna(how="all")


def write_differences(args: argparse.Namespace) -> None:
    results = {
        label: differing_rows(read_sorted(new, args.key), read_sorted(old, args.key))
        for label, new, old in args.pair
    }
    if args.output.suffix.lower() == ".csv":
        if len(results) != 1:
            raise ValueError("A CSV output supports one --pair; use an .xlsx file for several.")
        next(iter(results.values())).to_csv(args.output, index=False)
    else:
        with pd.ExcelWriter(args.output) as writer:
            for label, result in results.items():
                result.to_excel(writer, sheet_name=label[:31], index=False)
    print(f"Wrote differences for {len(results)} pair(s) to {args.output}")


def write_sources(args: argparse.Namespace) -> None:
    frames = []
    for label, filename in args.input:
        frame = read_sorted(filename, args.key).copy()
        frame[args.source_column] = label
        frames.append(frame)
    combined = pd.concat(frames, ignore_index=True).sort_values(args.key)
    if args.output.suffix.lower() == ".csv":
        combined.to_csv(args.output, index=False)
    else:
        combined.to_excel(args.output, index=False)
    print(f"Wrote {len(combined)} source-labelled row(s) to {args.output}")


def main() -> None:
    args = parse_args()
    if args.mode == "differences":
        write_differences(args)
    else:
        write_sources(args)


if __name__ == "__main__":
    main()
