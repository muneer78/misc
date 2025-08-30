import os

def extract_package_name(line):
    """
    Extracts the package name from an import statement.
    """
    parts = line.strip().split()
    if not parts:
        return None

    if parts[0] == "import":
        # Handles 'import package.subpackage'
        package_name = parts[1]
    elif parts[0] == "from" and len(parts) > 1:
        # Handles 'from package.subpackage import module'
        package_name = parts[1]
    else:
        return None

    # Extracts the base package name (e.g., 'os' from 'os.path')
    return package_name.split(".")[0]


def find_packages(directory):
    """
    Scans a directory for all Python files and extracts unique package names.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found at '{directory}'")
        return []

    packages = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as f:
                        for line in f:
                            if line.strip().startswith(("import ", "from ")):
                                package_name = extract_package_name(line)
                                if package_name and package_name not in ["os", "sys",
                                                                         "shutil"]:  # Exclude standard library modules
                                    packages.add(package_name)
                except UnicodeDecodeError:
                    print(f"Warning: Could not read file '{file_path}' (encoding issue). Skipping.")
    return sorted(list(packages))


def main():
    """
    Main function to run the package extraction process.
    """
    # Define the directory to scan (e.g., the current directory)
    directory_to_scan = "."

    # Find, deduplicate, and sort the package list
    package_list = find_packages(directory_to_scan)

    if package_list:
        print("Found the following unique packages:")
        for package in package_list:
            # The line below has been modified to wrap the package name in double quotes
            print(f'"{package}",')
    else:
        print("No third-party packages found in the directory.")


if __name__ == "__main__":
    main()