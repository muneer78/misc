"""Shared command-line selector for groups of scripts in this directory."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence


SUPPORTED_RUNNERS = {
    ".py": (sys.executable,),
    ".R": ("Rscript",),
    ".sh": ("sh",),
    ".pl": ("perl",),
}


def find_scripts(front_end: Path, prefixes: Sequence[str]) -> list[Path]:
    """Find runnable files whose names begin with one of the supplied prefixes."""
    front_end = front_end.resolve()
    directory = front_end.parent
    scripts = {
        path.resolve()
        for prefix in prefixes
        for path in directory.glob(f"{prefix}*")
        if path.is_file()
        and path.resolve() != front_end
        and path.suffix in SUPPORTED_RUNNERS
    }
    return sorted(scripts, key=lambda path: path.name.casefold())


def print_scripts(scripts: Sequence[Path]) -> None:
    for number, script in enumerate(scripts, start=1):
        print(f"{number:>2}. {script.name}")


def select_script(selector: str, scripts: Sequence[Path]) -> Path:
    """Resolve a menu number, filename, or unambiguous partial name."""
    if selector.isdigit():
        index = int(selector) - 1
        if 0 <= index < len(scripts):
            return scripts[index]
        raise ValueError(f"selection must be between 1 and {len(scripts)}")

    normalized = selector.casefold()
    exact_matches = [
        script
        for script in scripts
        if normalized in {script.name.casefold(), script.stem.casefold()}
    ]
    if exact_matches:
        return exact_matches[0]

    partial_matches = [
        script for script in scripts if normalized in script.name.casefold()
    ]
    if len(partial_matches) == 1:
        return partial_matches[0]
    if len(partial_matches) > 1:
        names = ", ".join(script.name for script in partial_matches)
        raise ValueError(f"'{selector}' is ambiguous; matches: {names}")
    raise ValueError(f"no script matches '{selector}'")


def command_for(script: Path, script_args: Sequence[str]) -> list[str]:
    runner = SUPPORTED_RUNNERS[script.suffix]
    executable = runner[0]
    if script.suffix != ".py" and shutil.which(executable) is None:
        raise RuntimeError(
            f"cannot run {script.name}: '{executable}' is not installed or not on PATH"
        )
    return [*runner, str(script), *script_args]


def run_selector(
    *, front_end: Path, prefixes: Sequence[str], category: str
) -> int:
    parser = argparse.ArgumentParser(
        description=f"Choose and run a {category} script from the text folder."
    )
    parser.add_argument(
        "script",
        nargs="?",
        help="script number, filename, stem, or an unambiguous part of its name",
    )
    parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        help="arguments to pass to the selected script",
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="list available scripts and exit"
    )
    args = parser.parse_args()

    scripts = find_scripts(front_end, prefixes)
    if not scripts:
        print(f"No runnable {category} scripts found.", file=sys.stderr)
        return 1

    if args.list:
        print_scripts(scripts)
        return 0

    selector = args.script
    if selector is None:
        if not sys.stdin.isatty():
            print("A script selection is required when input is not interactive.", file=sys.stderr)
            print("Use --list to see the available scripts.", file=sys.stderr)
            return 2
        print(f"Available {category} scripts:")
        print_scripts(scripts)
        try:
            selector = input("Select a script by number or name: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 130

    try:
        script = select_script(selector, scripts)
        command = command_for(script, args.script_args)
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    try:
        return subprocess.run(
            command, cwd=front_end.resolve().parent, check=False
        ).returncode
    except KeyboardInterrupt:
        return 130
