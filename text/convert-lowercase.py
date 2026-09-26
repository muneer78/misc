import subprocess


def copy_to_clipboard(text: str) -> None:
    """Copy text to the macOS clipboard."""
    subprocess.run(["pbcopy"], input=text, text=True, check=True)


def main() -> None:
    string = "SortandAddColumns"
    lowercase_string = string.lower()

    print(lowercase_string)
    copy_to_clipboard(lowercase_string)


if __name__ == "__main__":
    main()
