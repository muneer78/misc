#!/usr/bin/env python3
"""
Search for special characters below frontmatter in markdown files recursively.
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set


def extract_content_below_frontmatter(file_content: str) -> str:
    """
    Extract content below YAML frontmatter in a markdown file.

    Args:
        file_content (str): The full content of the markdown file

    Returns:
        str: Content below the frontmatter, or full content if no frontmatter found
    """
    # Pattern to match YAML frontmatter (--- at start, --- at end)
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'

    match = re.match(frontmatter_pattern, file_content, re.DOTALL)
    if match:
        # Return everything after the closing ---
        return file_content[match.end():]
    else:
        # No frontmatter found, return full content
        return file_content


def find_special_characters(text: str, custom_chars: Set[str] = None) -> Dict[str, List[Tuple[int, int]]]:
    """
    Find special characters in text and their positions.

    Args:
        text (str): Text to search in
        custom_chars (Set[str]): Custom set of characters to search for

    Returns:
        Dict[str, List[Tuple[int, int]]]: Dictionary mapping characters to list of (line, column) positions
    """
    if custom_chars is None:
        # Define common special characters to search for
        custom_chars = {
            '©', '®', '™', '§', '¶', '†', '‡', '•', '‰',
            '‹', '›', '«', '»','¡', '¿',
            '¢', '£', '¤', '¥', '¦', '©', 'ª', '«', '¬', '®', '¯',
            '°', '±', '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»',
            '¼', '½', '¾', '¿', 'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç',
            'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó',
            'Ô', 'Õ', 'Ö', '×', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß',
            # Add more Unicode special characters as needed
            '→', '←', '↑', '↓', '⇒', '⇐', '⇑', '⇓', '∞', '≠', '≤', '≥',
            '∑', '∏', '∫', '∆', '∇', '∂', '√', '∝', '∈', '∉', '∪', '∩'
        }

    found_chars = {}
    lines = text.split('\n')

    for line_num, line in enumerate(lines, 1):
        for col_num, char in enumerate(line, 1):
            if char in custom_chars:
                if char not in found_chars:
                    found_chars[char] = []
                found_chars[char].append((line_num, col_num))

    return found_chars


def search_markdown_files(directory: str, custom_chars: Set[str] = None, extensions: List[str] = None) -> Dict[
    str, Dict]:
    """
    Search for special characters in markdown files recursively.

    Args:
        directory (str): Root directory to search in
        custom_chars (Set[str]): Custom set of characters to search for
        extensions (List[str]): File extensions to search (default: ['.md', '.markdown'])

    Returns:
        Dict[str, Dict]: Dictionary mapping file paths to found characters and their positions
    """
    if extensions is None:
        extensions = ['.md', '.markdown']

    results = {}
    directory_path = Path(directory)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist")

    if not directory_path.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory")

    # Find all markdown files recursively
    for file_path in directory_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Extract content below frontmatter
                content_below_frontmatter = extract_content_below_frontmatter(content)

                # Search for special characters
                found_chars = find_special_characters(content_below_frontmatter, custom_chars)

                if found_chars:
                    results[str(file_path)] = {
                        'characters': found_chars,
                        'total_occurrences': sum(len(positions) for positions in found_chars.values())
                    }

            except Exception as e:
                print(f"Error reading file '{file_path}': {e}")

    return results


def print_results(results: Dict[str, Dict], show_positions: bool = True):
    """
    Print search results in a formatted way.

    Args:
        results (Dict[str, Dict]): Search results
        show_positions (bool): Whether to show character positions
    """
    if not results:
        print("No special characters found in any markdown files.")
        return

    print(f"Found special characters in {len(results)} file(s):\n")

    for file_path, data in results.items():
        print(f"📄 {file_path}")
        print(f"   Total occurrences: {data['total_occurrences']}")

        for char, positions in data['characters'].items():
            print(f"   '{char}' (Unicode: U+{ord(char):04X}): {len(positions)} occurrence(s)")
            if show_positions and len(positions) <= 10:  # Limit output for readability
                for line, col in positions:
                    print(f"      Line {line}, Column {col}")
            elif show_positions and len(positions) > 10:
                print(f"      First 10 positions:")
                for line, col in positions[:10]:
                    print(f"      Line {line}, Column {col}")
                print(f"      ... and {len(positions) - 10} more")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Search for special characters below frontmatter in markdown files recursively"
    )
    parser.add_argument(
        "directory",
        help="Directory to search in",
        default="/Users/muneer78/Documents/GitHub/mun-ssg/content",
        nargs="?"
    )
    parser.add_argument(
        "--chars",
        help="Custom characters to search for (as a string)",
        default=None
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        help="File extensions to search (default: .md .markdown)",
        default=['.md', '.markdown']
    )
    parser.add_argument(
        "--no-positions",
        action="store_true",
        help="Don't show character positions"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show only summary statistics"
    )

    args = parser.parse_args()

    # Parse custom characters if provided
    custom_chars = None
    if args.chars:
        custom_chars = set(args.chars)

    try:
        results = search_markdown_files(
            args.directory,
            custom_chars=custom_chars,
            extensions=args.extensions
        )

        if args.summary:
            total_files = len(results)
            total_chars = sum(len(data['characters']) for data in results.values())
            total_occurrences = sum(data['total_occurrences'] for data in results.values())

            print(f"Summary:")
            print(f"  Files with special characters: {total_files}")
            print(f"  Unique special characters found: {total_chars}")
            print(f"  Total occurrences: {total_occurrences}")
        else:
            print_results(results, show_positions=not args.no_positions)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()