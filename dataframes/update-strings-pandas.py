import pandas as pd
import re


def process_text(text):
    pattern = r"(.+? LLC)"
    match = re.search(pattern, text)
    return match.group(1).strip().upper() if match else text.upper()


def convert_ar_to_integer(value, column_name):
    if column_name == "AR" and isinstance(value, str):
        # Replace 'k' or 'K' at the end of the string with '000' only for 'AR' column
        value = re.sub(r"([kK])$", r"000", value)
        # Extract numeric part
        numeric_part = re.search(r"\d+", value)
        if numeric_part:
            return int(numeric_part.group())
    return value


def write_output_to_csv(df, output_csv_path):
    df.to_csv(output_csv_path, index=False)


def main():
    excel_file_path = "concentrations.xlsx"
    output_csv_path = "output_file.csv"

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path)

    # Filter rows where the value in the "Include" column is 1
    df = df[df["Include"] == 1]

    # Convert values in the 'AR' column matching the pattern to integers
    df["AR"] = df.apply(lambda row: convert_ar_to_integer(row["AR"], "AR"), axis=1)

    # Convert 'Date Added' and 'FF Date' columns to datetime with 'YYYY-MM-DD' format
    df["Date Added"] = pd.to_datetime(df["Date Added"]).dt.strftime("%Y-%m-%d")
    df["FF Date"] = pd.to_datetime(df["FF Date"]).dt.strftime("%Y-%m-%d")

    # Sort the DataFrame by 'Client Name' and then 'Debtor'
    df = df.sort_values(by=["Client Name", "Debtor"])

    # Drop the original 'Include' column
    df.drop("Include", axis=1, inplace=True)

    # Write the processed DataFrame to a CSV file
    write_output_to_csv(df, output_csv_path)


if __name__ == "__main__":
    main()
