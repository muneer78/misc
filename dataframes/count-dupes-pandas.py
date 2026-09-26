from pathlib import Path
import pandas as pd
from rich import print


def main():
    # Set the directory containing the cleaned CSV files
    data_dir = Path(
        r"C:\Users\mahmad\OneDrive - Ryan RTS\Downloads"
    )  # Replace with your directory path

    if not data_dir.is_dir():
        print(f"[red]Error: The directory {data_dir} does not exist.[/red]")
        return

    # Define file paths
    df1_filename = data_dir / "active_auth_count.csv"

    # Read DataFrames
    df1 = pd.read_csv(df1_filename)

    # Count duplicate values in transaction ID columns
    df1_id_dupes = len(df1["dotnbr"]) - len(df1["dotnbr"].drop_duplicates())
    print(f"Number of duplicates: {df1_id_dupes}")


if __name__ == "__main__":
    main()
