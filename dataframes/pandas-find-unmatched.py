from pathlib import Path
import pandas as pd
from rich import print


def main():
    # Set the directory containing the cleaned CSV files
    data_dir = Path(
        r"C:\Users\mahmad\OneDrive - Ryan RTS\code"
    )  # Replace with your directory path

    if not data_dir.is_dir():
        print(f"[red]Error: The directory {data_dir} does not exist.[/red]")
        return

    # Define file paths
    df1_cleaned_filename = data_dir / "df1_cleaned.csv"
    df2_cleaned_filename = data_dir / "df2_cleaned.csv"

    if not df1_cleaned_filename.exists() or not df2_cleaned_filename.exists():
        print(f"[red]Error: One or more files do not exist in {data_dir}.[/red]")
        return

    # Read cleaned DataFrames
    df1_cleaned = pd.read_csv(df1_cleaned_filename)
    df2_cleaned = pd.read_csv(df2_cleaned_filename)

    # Find records in DF1 but not in DF2
    df1_not_in_df2 = df1_cleaned[~df1_cleaned["id"].isin(df2_cleaned["id"])].copy()
    df2_not_in_df1 = df2_cleaned[~df2_cleaned["id"].isin(df1_cleaned["id"])].copy()

    # Add a source column to each unmatched DataFrame
    df1_not_in_df2["source"] = "df1_not_in_df2"
    df2_not_in_df1["source"] = "df2_not_in_df1"

    # Combine unmatched records into one DataFrame
    combined_unmatched = pd.concat([df1_not_in_df2, df2_not_in_df1], ignore_index=True)

    # Define output file path
    output_file = data_dir / "combined_unmatched_records.csv"

    # Save combined unmatched records to a CSV file
    combined_unmatched.to_csv(output_file, index=False)

    # Print counts and confirmation
    print(
        f"[green]Count of records in DF1 but not in DF2:[/green] {len(df1_not_in_df2)}"
    )
    print(
        f"[green]Count of records in DF2 but not in DF1:[/green] {len(df2_not_in_df1)}"
    )
    print(f"[blue]Combined unmatched records saved to:[/blue] {output_file}")


if __name__ == "__main__":
    main()
