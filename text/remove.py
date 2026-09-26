#!/usr/bin/env python3
"""Select and run a remove-prefixed script."""

from pathlib import Path

from _script_selector import run_selector


if __name__ == "__main__":
    raise SystemExit(
        run_selector(front_end=Path(__file__), prefixes=("remove",), category="remove")
    )
