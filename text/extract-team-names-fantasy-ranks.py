#!/usr/bin/env python3
"""
Markdown Team Ranking Extractor

Extracts team rankings from markdown files that contain patterns like:
### **1. [Philadelphia Eagles](link)**
### **2. Denver Broncos**
**1. Philadelphia Eagles**

Outputs results as CSV with rank and team columns.
"""

import re
import csv
import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Optional


def extract_rankings(content: str) -> List[Tuple[int, str]]:
    """
    Extract team rankings from markdown content.

    Args:
        content: The markdown content as a string

    Returns:
        List of tuples containing (rank, team_name)
    """
    rankings = []

    # Multiple patterns to catch different markdown formats
    patterns = [
        # ### **1. [Philadelphia Eagles](link)**
        r'###\s*\*\*(\d+)\.\s*\[([^\]]+)\]',

        # ### **1. Philadelphia Eagles**
        r'###\s*\*\*(\d+)\.\s*([^*\n]+?)\*\*',

        # ### 1. Philadelphia Eagles (without bold)
        r'###\s*(\d+)\\?\.\s*([^\n]+?)(?:\n|$)',

        # **1. Philadelphia Eagles**
        r'^\*\*(\d+)\.\s*([^*\n]+?)\*\*',

        # ## 32) Houston Texans or ## 1) Denver Broncos
        r'##\s*(\d+)\)\s*([^\n]+)',

        # ## 1. Philadelphia Eagles
        r'##\s*(\d+)\.\s*([^\n]+)',

        # # 1. Philadelphia Eagles
        r'#\s*(\d+)\.\s*([^\n]+)',

        # 1. **Philadelphia Eagles**
        r'^(\d+)\.\s*\*\*([^*\n]+?)\*\*',

        # Simple numbered list: 1. Philadelphia Eagles
        r'^(\d+)\.\s*([A-Za-z][^\n]+?)(?:\n|$)',
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            try:
                rank = int(match.group(1))
                team = match.group(2).strip()

                # Clean up team name
                team = clean_team_name(team)

                # Skip if team name is too short or invalid
                if team and len(team) > 2 and is_valid_team_name(team):
                    rankings.append((rank, team))
            except (ValueError, IndexError):
                continue

    # Remove duplicates, keeping the first occurrence of each rank
    seen_ranks = set()
    unique_rankings = []

    for rank, team in sorted(rankings):
        if rank not in seen_ranks:
            seen_ranks.add(rank)
            unique_rankings.append((rank, team))

    return sorted(unique_rankings)


def clean_team_name(team: str) -> str:
    """Clean up extracted team name."""
    # Remove HTML tags
    team = re.sub(r'<[^>]*>', '', team)

    # Remove markdown formatting
    team = re.sub(r'\*+', '', team)
    team = re.sub(r'_+', '', team)

    # Remove extra whitespace
    team = ' '.join(team.split())

    # Remove trailing punctuation (but keep apostrophes within names)
    team = re.sub(r'[^\w\s\']+$', '', team)

    return team.strip()


def is_valid_team_name(team: str) -> bool:
    """Check if the extracted text looks like a valid team name."""
    # Skip obvious non-team patterns
    invalid_patterns = [
        r'^(subscribe|get|access|rankings|more|the|and|or|but|with|for|to|in|at|on|of)$',
        r'^\d+$',
        r'^[a-z]+$',  # All lowercase (likely not a team name)
        r'pff|grade|season|year|football|nfl'
    ]

    team_lower = team.lower()
    for pattern in invalid_patterns:
        if re.search(pattern, team_lower):
            return False

    # Must contain at least one uppercase letter (team names are proper nouns)
    if not re.search(r'[A-Z]', team):
        return False

    return True


def save_to_csv(rankings: List[Tuple[int, str]], output_file: str) -> None:
    """Save rankings to CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['rank', 'team'])
        writer.writerows(rankings)


def print_rankings(rankings: List[Tuple[int, str]]) -> None:
    """Print rankings to console in CSV format."""
    print("rank,team")
    for rank, team in rankings:
        # Escape team names that contain commas
        if ',' in team:
            team = f'"{team}"'
        print(f"{rank},{team}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract team rankings from markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_rankings.py rankings.md
  python extract_rankings.py rankings.md -o output.csv
  python extract_rankings.py rankings.md --preview
        """
    )

    parser.add_argument('input_file', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output CSV file (default: print to console)')
    parser.add_argument('--preview', action='store_true', help='Preview results without saving')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Check if input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Read the markdown file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Reading from: {input_path}")
        print(f"File size: {len(content)} characters")

    # Extract rankings
    rankings = extract_rankings(content)

    if not rankings:
        print("No team rankings found in the file!", file=sys.stderr)
        print("Make sure the file contains patterns like:")
        print("  ### **1. Philadelphia Eagles**")
        print("  **1. Philadelphia Eagles**")
        print("  1. Philadelphia Eagles")
        sys.exit(1)

    if args.verbose:
        print(f"Found {len(rankings)} team rankings")

    # Output results
    if args.preview:
        print("Preview of extracted rankings:")
        print("-" * 30)
        print_rankings(rankings)
    elif args.output:
        save_to_csv(rankings, args.output)
        print(f"Rankings saved to: {args.output}")
        if args.verbose:
            print(f"Extracted {len(rankings)} teams")
    else:
        print_rankings(rankings)


if __name__ == "__main__":
    main()