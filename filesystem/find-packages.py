import os
import ast


def find_python_packages(folder_path):
    packages = set()
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    packages.add(alias.name.split(".")[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    packages.add(node.module.split(".")[0])
                    except Exception:
                        continue
    return sorted(packages)


if __name__ == "__main__":
    folder = "/Users/muneer78/files/scripts"
    pkgs = find_python_packages(folder)
    with open("uv-packages.toml", "w", encoding="utf-8") as f:
        f.write("[dependencies]\n")
        f.write("packages = [\n")
        for pkg in pkgs:
            f.write(f'    "{pkg}",\n')
        f.write("]\n")
