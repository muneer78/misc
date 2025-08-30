import subprocess
from pathlib import Path


def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        subprocess.run(["python", script_name], check=True)
        print(f"{script_name} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
        exit(1)


if __name__ == "__main__":
    # Set the directory where the scripts are located
    scripts_dir = Path(
        r"C:\Users\mahmad\OneDrive - Ryan RTS\code"
    )  # Replace with your scripts directory
    if not scripts_dir.is_dir():
        print(f"The directory {scripts_dir} does not exist.")
        exit(1)

    # Change the working directory
    print(f"Changing working directory to {scripts_dir}\n")
    Path.cwd().joinpath(scripts_dir).resolve()

    # Run the scripts
    run_script(scripts_dir / "pandas-count-dupes.py")
    run_script(scripts_dir / "pandas-find-unmatched.py")
