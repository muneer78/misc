#!/usr/bin/env python3
"""Flatten JSON values stored in selected columns of a CSV file.

Example:
    python json-flatten.py input.csv output.csv --field pickup --field delivery
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


def flatten_json(value: Any, prefix: str = "") -> dict[str, Any]:
    """Return a flat mapping for nested dictionaries and lists.

    Dictionary keys are joined with underscores and list indexes become part of
    the key, e.g. ``{"pickup": [{"time": "08:00"}]}`` becomes
    ``{"pickup_0_time": "08:00"}``.
    """
    flattened: dict[str, Any] = {}

    def visit(item: Any, path: str) -> None:
        if isinstance(item, dict):
            for key, child in item.items():
                visit(child, f"{path}_{key}" if path else str(key))
        elif isinstance(item, list):
            for index, child in enumerate(item):
                visit(child, f"{path}_{index}" if path else str(index))
        elif path:
            flattened[path] = item

    visit(value, prefix)
    return flattened


def parse_json(value: Any) -> Any | None:
    """Parse a JSON string, ignoring blank, missing, and invalid values."""
    if not isinstance(value, str) or not value.strip():
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def flatten_columns(df: pd.DataFrame, fields: list[str]) -> pd.DataFrame:
    """Add flattened columns for each requested JSON column."""
    missing_fields = [field for field in fields if field not in df.columns]
    if missing_fields:
        available = ", ".join(df.columns)
        missing = ", ".join(missing_fields)
        raise ValueError(f"Column(s) not found: {missing}. Available: {available}")

    result = df.copy()
    for field in fields:
        expanded_rows = [
            {f"{field}_{key}": item for key, item in flatten_json(parsed).items()}
            if (parsed := parse_json(value)) is not None
            else {}
            for value in result[field]
        ]
        expanded = pd.DataFrame(expanded_rows, index=result.index)
        result = pd.concat([result, expanded], axis=1)

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path, help="CSV file containing JSON columns")
    parser.add_argument("output_csv", type=Path, help="Destination for the expanded CSV")
    parser.add_argument(
        "--field",
        dest="fields",
        action="append",
        required=True,
        help="JSON column to flatten; repeat for multiple columns",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataframe = pd.read_csv(args.input_csv)
    flattened = flatten_columns(dataframe, args.fields)
    flattened.to_csv(args.output_csv, index=False)

    field_counts = flattened.count(axis=1)
    print(f"Updated CSV written to {args.output_csv}")
    print(f"Minimum number of fields in a single record: {field_counts.min()}")
    print(f"Maximum number of fields in a single record: {field_counts.max()}")


if __name__ == "__main__":
    main()
