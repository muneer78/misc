import pandas as pd
from datetime import datetime
import glob


def find_matching_file(pattern):
    files = glob.glob("*.xlsx")
    for file in files:
        if pattern in file:
            return file


def read_excel(filename, sheet_name):
    return pd.read_excel(filename, sheet_name=sheet_name)


def export_to_csv(dataframe, filename_prefix):
    current_date = datetime.now().strftime("%Y-%m-%d")
    dataframe.to_csv(f"{current_date}-{filename_prefix}.csv", index=False)


def main():
    # Find matching file
    filename = find_matching_file("Operation Local Language - MASTER LIST")

    # Read data from different sheets
    sheet_names = ["Week 2", "Week 3", "Week 4", "Extra Credit"]
    dataframes = {
        sheet_name: read_excel(filename, sheet_name) for sheet_name in sheet_names
    }

    # Export dataframes to CSV files
    for sheet_name, dataframe in dataframes.items():
        export_to_csv(dataframe, sheet_name.replace(" ", ""))


if __name__ == "__main__":
    main()
