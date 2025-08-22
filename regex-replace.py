import re


def replace_in_file(filepath, pattern, replacement):
    """Replaces occurrences of a pattern in a file, preserving case."""
    try:
        with open(filepath, "r") as f:
            file_content = f.read()

        new_content = re.sub(pattern, replacement, file_content)

        with open(filepath, "w") as f:
            f.write(new_content)

        print(f"Replacements made successfully in {filepath}")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage (preserving case):
filepath = (
    "/Users/muneer78/Downloads/convert/who-goes-maga.md"  # Replace with your file path
)
pattern = r"Mr\.\s.{2}"  # Your regex pattern
replacement = r"* \g *"  # Your replacement string (e.g., surrounding with asterisks)

replace_in_file(filepath, pattern, replacement)

# Example usage with a function (preserving case):


def replace_function(match):
    matched_string = match.group(0)
    return f"**{matched_string}**"  # Just bold, no uppercase


replace_in_file(filepath, pattern, replace_function)


# Dry run example (also preserving case):
def dry_run_replace(filepath, pattern, replacement):
    try:
        with open(filepath, "r") as f:
            file_content = f.read()

        new_content = re.sub(pattern, replacement, file_content)

        print("--- Dry Run Results ---")
        print(new_content)
        print("--- End of Dry Run ---")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


dry_run_replace(filepath, pattern, replacement)  # Example dry run usage
