"""Join or concatenate CSV files with Polars."""

from __future__ import annotations

import argparse
from pathlib import Path

import polars as pl


def parse_value(value: str) -> object:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def parse_condition(value: str) -> tuple[str, object]:
    try:
        column, expected = value.split("=", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use COLUMN=VALUE") from error
    if not column:
        raise argparse.ArgumentTypeError("Use COLUMN=VALUE")
    return column, parse_value(expected)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Join or concatenate CSV files.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    join = subparsers.add_parser("join", help="Join two CSV files")
    join.add_argument("left", type=Path)
    join.add_argument("right", type=Path)
    join.add_argument("-o", "--output", type=Path, required=True)
    join.add_argument("--on", help="Shared join column")
    join.add_argument("--left-on", help="Join column in the left file")
    join.add_argument("--right-on", help="Join column in the right file")
    join.add_argument(
        "--how", default="inner", choices=["inner", "left", "right", "full", "semi", "anti"]
    )
    join.add_argument(
        "--left-not-null", action="append", default=[], help="Left-side column that must not be null"
    )
    join.add_argument(
        "--right-where", action="append", default=[], type=parse_condition,
        metavar="COLUMN=VALUE", help="Keep right-side rows matching this condition"
    )
    join.add_argument("--unique", action="store_true", help="Remove duplicate result rows")

    concat = subparsers.add_parser("concat", help="Concatenate CSV files")
    concat.add_argument("files", nargs="+", type=Path)
    concat.add_argument("-o", "--output", type=Path, required=True)
    concat.add_argument(
        "--not-null", action="append", default=[], help="Keep rows where this column is not null"
    )
    concat.add_argument(
        "--cast-int", action="append", default=[], help="Cast this column to Int64"
    )
    return parser.parse_args()


def join_files(args: argparse.Namespace) -> None:
    if bool(args.left_on) != bool(args.right_on) and not args.on:
        raise ValueError("Provide both --left-on and --right-on, or provide --on.")
    if args.on and (args.left_on or args.right_on):
        raise ValueError("Use either --on or --left-on/--right-on.")
    if not args.on and not args.left_on:
        raise ValueError("A join key is required: --on or --left-on/--right-on.")

    left, right = pl.read_csv(args.left), pl.read_csv(args.right)
    for column in args.left_not_null:
        left = left.filter(pl.col(column).is_not_null())
    for column, value in args.right_where:
        right = right.filter(pl.col(column) == value)

    if args.on:
        result = left.join(right, on=args.on, how=args.how)
    else:
        result = left.join(right, left_on=args.left_on, right_on=args.right_on, how=args.how)
    if args.unique:
        result = result.unique()
    result.write_csv(args.output)
    print(f"Wrote {result.height} joined row(s) to {args.output}")


def concat_files(args: argparse.Namespace) -> None:
    combined = pl.concat([pl.read_csv(filename) for filename in args.files], how="diagonal_relaxed")
    initial_count = combined.height
    for column in args.not_null:
        combined = combined.filter(pl.col(column).is_not_null())
    if args.cast_int:
        combined = combined.with_columns(
            [pl.col(column).cast(pl.Int64) for column in args.cast_int]
        )
    combined.write_csv(args.output)
    print(f"Combined {len(args.files)} file(s): {initial_count} row(s) read.")
    print(f"Rows removed: {initial_count - combined.height}")
    print(f"Wrote {combined.height} row(s) to {args.output}")


def main() -> None:
    args = parse_args()
    if args.mode == "join":
        join_files(args)
    else:
        concat_files(args)


if __name__ == "__main__":
    main()
