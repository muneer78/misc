import pandas as pd
from datetime import datetime as dt
import glob

date_today = dt.now().strftime("%m-%d-%Y")


def find_file(pattern):
    files = glob.glob("*.xlsx")
    for file in files:
        if pattern in file:
            return file


def read_excel_sheet(filename, sheet_name):
    return pd.read_excel(filename, sheet_name=sheet_name)


# def process_external_data(df):
#     if "DataLoad" in df.columns:
#         filtered_df = df[df["DataLoad"] == "Y"].copy()
#         filtered_df["RecordTypeId"] = "0123x000001RlZ6AAK"
#         filtered_df["RTSCSOpsReview"] = "Complete"
#         filtered_df["Established Date"] = filtered_df["Fuel Discount Applied"]
#         return filtered_df
#     else:
#         raise ValueError("DataLoad column not found in the input data")


def process_internalpilot_data(df):
    if "DataLoad" in df.columns:
        filtered_df = df[df["DataLoad"] == "Y"].copy()
        filtered_df["RecordTypeId"] = "0123x000001RlZ7AAK"
        filtered_df["Status"] = "Processing"

        # Renaming column 'A' to 'New_Column'
        filtered_df = filtered_df.rename(
            columns={"Proposal Completed Date": "Proposal Received Date"}
        )

        return filtered_df
    else:
        raise ValueError("DataLoad column not found in the input data")


def process_innetwork_data(df):
    if "DataLoad" in df.columns:
        filtered_df = df[df["DataLoad"] == "Y"].copy()
        filtered_df["RecordTypeId"] = "0123x000001RlZ7AAK"
        filtered_df["Fuel Discount Applied"] = date_today
        filtered_df["Established Date"] = date_today
        filtered_df["RTSCSOpsReview"] = "Complete"
        return filtered_df
    else:
        raise ValueError("DataLoad column not found in the input data")


def fuelcard_update(df):
    if "DataLoad" in df.columns:
        filtered_df = df[df["DataLoad"] == "Y"].copy()
        filtered_df["MinGalPercentage"] = 90
        filtered_df["Bundle Start Date"] = date_today
        filtered_df["Fuel Card Bundle Status"] = "Active"

        # Renaming column 'RTSF Bundle Date' to 'Bundle Start Date'
        filtered_df = filtered_df.rename(columns={"Status": "Bundle Status"})

        return filtered_df
    else:
        raise ValueError("DataLoad column not found in the input data")


def export_to_csv(data_frame, filename_prefix, columns_to_export):
    data_frame[columns_to_export].to_csv(
        f"{date_today}-{filename_prefix}.csv", index=False
    )


def main():
    # Find matching file
    filename = find_file("20230926 Factoring Bundles")
    sheet_names = [
        "Listed as External Bundle",
        "Listed as Internal-Pilot Bundle",
        "Listed as In-Network Bundle",
    ]
    dfs = {
        sheet_name: read_excel_sheet(filename, sheet_name) for sheet_name in sheet_names
    }
    # df_external = dfs["Listed as External Bundle"]
    df_pilot = dfs["Listed as Internal-Pilot Bundle"]
    df_innetwork = dfs["Listed as In-Network Bundle"]

    # # Process external data
    # result_external = process_external_data(df_external)
    # external_columns = [
    #     "Bundle Type",
    #     "Fuel Opp ID",
    #     "Fuel Card ID",
    #     "RTSF Opp ID",
    #     "Account Name",
    #     "Account ID",
    #     "Proposal Sent Date",
    #     "Proposal Completed Date",
    #     "Established Date",
    #     "RTSF Contract ID",
    #     "Fuel Discount",
    #     "Fuel Discount Applied",
    #     "Status",
    #     "RTSCSOpsReview",
    #     "RecordTypeId",
    # ]

    result_internalpilot = process_internalpilot_data(df_pilot)
    internalpilot_columns = [
        "Bundle Type",
        "Fuel Opp ID",
        "Fuel Card ID",
        "RTSF Opp ID",
        "Account Name",
        "Account ID",
        "Proposal Sent Date",
        "RTSF Contract ID",
        "Status",
        "RecordTypeId",
        "Proposal Received Date",
        "Established Date",
    ]

    result_fuel_card = fuelcard_update(df_innetwork)
    fuel_card_update_columns = [
        "Bundle Type",
        "Fuel Card ID",
        "Fuel Card Bundle Status",
        "Bundle Start Date",
        "MinGalPercentage",
    ]

    result_innetwork = process_innetwork_data(df_innetwork)
    innetwork_columns = [
        "Bundle Type",
        "Fuel Opp ID",
        "Fuel Card ID",
        "RTSF Opp ID",
        "Account Name",
        "Account ID",
        "Proposal Sent Date",
        "Proposal Completed Date",
        "Established Date",
        "RTSF Contract ID",
        "Fuel Discount",
        "Fuel Discount Applied",
        "Status",
        "RTSCSOpsReview",
        "RecordTypeId",
    ]

    # Export processed external data with specific columns to CSV
    # export_to_csv(result_external, "External", external_columns)
    export_to_csv(result_internalpilot, "Internal Pilot", internalpilot_columns)
    export_to_csv(result_fuel_card, "In Network Fuel Cards", fuel_card_update_columns)
    export_to_csv(result_innetwork, "In Network", innetwork_columns)


if __name__ == "__main__":
    main()
