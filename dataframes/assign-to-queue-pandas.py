"""Assign records to queue members in round-robin order."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def parse_field(value: str) -> tuple[str, str]:
    try:
        column, field_value = value.split("=", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use COLUMN=VALUE") from error
    if not column:
        raise argparse.ArgumentTypeError("Use COLUMN=VALUE")
    return column, field_value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assign records to queue members in round-robin order."
    )
    parser.add_argument("--input", type=Path, required=True, help="Input CSV or Excel file")
    parser.add_argument("--sheet", help="Excel sheet name (required for a multi-sheet workbook)")
    parser.add_argument("--output", type=Path, required=True, help="Output CSV or Excel file")
    parser.add_argument("--output-sheet", default="Assigned Records")
    parser.add_argument(
        "--assignments",
        type=Path,
        required=True,
        help='JSON file mapping buckets to assignee lists, e.g. {"AZ 1-9": ["Ava"]}',
    )
    parser.add_argument("--bucket-column", default="bucket")
    parser.add_argument("--assignee-column", default="rep")
    parser.add_argument("--rep-list", type=Path, help="CSV containing rep names and IDs")
    parser.add_argument("--rep-name-column", default="Name")
    parser.add_argument("--rep-id-column", default="ID")
    parser.add_argument("--assignee-id-column", default="repid")
    parser.add_argument("--state-column", help="Create territory buckets using this state column")
    parser.add_argument("--size-column", help="Create territory buckets using this numeric column")
    parser.add_argument("--territory-states", default="AZ,GA,IL,TN,TX")
    parser.add_argument("--non-territory-prefix", default="NR")
    parser.add_argument(
        "--set", action="append", default=[], type=parse_field, metavar="COLUMN=VALUE",
        help="Set a constant output column; may be repeated",
    )
    return parser.parse_args()


def read_input(filename: Path, sheet: str | None) -> pd.DataFrame:
    if filename.suffix.lower() in {".xlsx", ".xls", ".xlsm"}:
        return pd.read_excel(filename, sheet_name=sheet if sheet else 0)
    return pd.read_csv(filename)


def territory_bucket(
    state: object, size: object, territory_states: set[str], non_territory_prefix: str
) -> str:
    if pd.isna(size):
        return "not processed"
    size = float(size)
    if size > 40:
        return "40+"
    if size < 0:
        return "not processed"
    prefix = str(state).upper() if str(state).upper() in territory_states else non_territory_prefix
    if size <= 9:
        return f"{prefix} 1-9"
    if size <= 25:
        return f"{prefix} 10-25"
    return f"{prefix} 26-40"


def load_assignments(filename: Path) -> dict[str, list[str]]:
    with filename.open(encoding="utf-8") as file:
        assignments = json.load(file)
    if not isinstance(assignments, dict) or any(
        not isinstance(bucket, str) or not isinstance(reps, list) or not reps
        for bucket, reps in assignments.items()
    ):
        raise ValueError("Assignments must be a JSON object of non-empty assignee lists.")
    return assignments


def assign_round_robin(
    frame: pd.DataFrame, assignments: dict[str, list[str]], bucket_column: str, assignee_column: str
) -> pd.DataFrame:
    if bucket_column not in frame.columns:
        raise ValueError(f"Bucket column not found: {bucket_column}")
    result = frame.copy()
    result[assignee_column] = pd.NA
    for bucket, indexes in result.groupby(bucket_column, dropna=False).groups.items():
        assignees = assignments.get(bucket, [])
        if assignees:
            result.loc[indexes, assignee_column] = [
                assignees[position % len(assignees)] for position in range(len(indexes))
            ]
    return result


def main() -> None:
    args = parse_args()
    frame = read_input(args.input, args.sheet)
    if bool(args.state_column) != bool(args.size_column):
        raise ValueError("Use --state-column and --size-column together.")
    if args.state_column:
        missing = {args.state_column, args.size_column} - set(frame.columns)
        if missing:
            raise ValueError(f"Missing territory column(s): {', '.join(sorted(missing))}")
        territory_states = {state.strip().upper() for state in args.territory_states.split(",")}
        frame[args.bucket_column] = frame.apply(
            lambda row: territory_bucket(
                row[args.state_column], row[args.size_column], territory_states, args.non_territory_prefix
            ),
            axis=1,
        )

    result = assign_round_robin(
        frame, load_assignments(args.assignments), args.bucket_column, args.assignee_column
    )
    if args.rep_list:
        reps = pd.read_csv(args.rep_list)
        required = {args.rep_name_column, args.rep_id_column}
        if not required.issubset(reps.columns):
            raise ValueError(f"Rep list must include: {', '.join(sorted(required))}")
        rep_ids = reps.set_index(args.rep_name_column)[args.rep_id_column]
        result[args.assignee_id_column] = result[args.assignee_column].map(rep_ids)
    for column, value in args.set:
        result[column] = value

    if args.output.suffix.lower() == ".csv":
        result.to_csv(args.output, index=False)
    else:
        result.to_excel(args.output, sheet_name=args.output_sheet, index=False)
    assigned = result[args.assignee_column].notna().sum()
    print(f"Assigned {assigned} of {len(result)} record(s); wrote {args.output}")


if __name__ == "__main__":
    main()
