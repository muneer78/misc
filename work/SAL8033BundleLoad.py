import pandas as pd
from datetime import datetime as dt
import glob

date_today = dt.now().strftime("%m-%d-%Y")

internalpilot_columns = [
    "Bundle Type",
    "CS Opportunity ID",
    "Fuel Card ID",
    "RTSF Opportunity ID",
    "Account Name/Bundle Object Name",
    "Account ID",
    "Proposal Sent Date",
    "RTSF Contract ID",
    "Status",
    "Proposal Received Date",
    "Established Date",
    "Fuel Discount",
    "Fuel Discount Applied",
    "RTSCS Ops Review",
    "PFJ Review",
    "PFJ Response",
    "Time",
    "RecordTypeId",  # Added RecordTypeId to internalpilot_columns
]

innetwork_columns = [
    "Bundle Type",
    "CS Opportunity ID",
    "Fuel Card ID",
    "RTSF Opportunity ID",
    "Account Name/Bundle Object Name",
    "Account ID",
    "Proposal Sent Date",
    "Proposal Received Date",
    "Established Date",
    "RTSF Contract ID",
    "Fuel Discount",
    "Fuel Discount Applied",
    "Status",
    "RTSCS Ops Review",
    "RecordTypeId",  # Added RecordTypeId to innetwork_columns
]

sheetname_mapping = {
    "Internal-Pilot Load": "internalpilot",
    "In-Network Load": "innetwork",
}


def find_matching_file(pattern):
    files = glob.glob("*.xlsx")
    for file in files:
        if pattern in file:
            return file


def read_excel(filename, sheet_name, columns):
    df = pd.read_excel(filename, sheet_name=sheet_name)
    df.columns = [
        col.strip() for col in df.columns
    ]  # Stripping spaces from column names
    df = df[[col.strip() for col in columns]]  # Stripping spaces from specified columns
    return df


def process_internalpilot_data(df):
    df["RecordTypeId"] = "0123x000001RlZ7AAK"
    return df


def process_innetwork_data(df):
    df["RecordTypeId"] = "0123x000001RlZ7AAK"
    return df


def export_to_csv(data_frame, filename_prefix, columns_to_export):
    data_frame.to_csv(
        f"{date_today}-{filename_prefix}.csv", index=False, columns=columns_to_export
    )


def main():
    # Find matching file
    filename = find_matching_file("non-combined 1-1 bundle")
    if filename is None:
        print("No matching file found.")
        return

    # Read data from different sheets
    sheet_names = ["Internal-Pilot Load", "In-Network Load"]
    dfs = {
        sheetname_mapping[sheet_name]: read_excel(filename, sheet_name, columns)
        for sheet_name, columns in zip(
            sheet_names, [internalpilot_columns, innetwork_columns]
        )
    }

    df_pilot = dfs["internalpilot"]
    df_innetwork = dfs["innetwork"]

    result_innetwork = process_innetwork_data(df_innetwork)
    result_internalpilot = process_internalpilot_data(df_pilot)

    export_to_csv(result_internalpilot, "Internal Pilot", internalpilot_columns)
    export_to_csv(result_innetwork, "In Network", innetwork_columns)


if __name__ == "__main__":
    main()
