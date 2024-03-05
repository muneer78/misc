import datetime
import pandas as pd


def calculate_success_rate(successful_records, errored_records):
    """
    Calculates the success rate based on successful and errored records.
    """
    total_records = successful_records + errored_records
    if total_records == 0:
        return 0.0
    return (successful_records / total_records) * 100


def main():
    # Initialize empty lists to store data
    dates = []
    successful_records_list = []
    errored_records_list = []
    names = ["Leads", "New Opportunities", "Reassigned Opportunities"]

    # Input data for three rows
    for i in range(3):
        date = datetime.date.today().strftime("%m-%d-%Y")  # Get the current date
        successful_records = int(input("Enter the number of successful records: "))
        errored_records = int(input("Enter the number of errored records: "))

        # Calculate success rate
        success_rate = calculate_success_rate(successful_records, errored_records)

        # Append data to lists
        dates.append(date)
        successful_records_list.append(successful_records)
        errored_records_list.append(errored_records)

    # Create a DataFrame
    data = {
        "Name": names,
        "Date": dates,
        "Successful Records": successful_records_list,
        "Errored Records": errored_records_list,
    }
    df = pd.DataFrame(data)

    # Calculate success rate and add to DataFrame
    df["Success Rate"] = df.apply(
        lambda row: calculate_success_rate(
            row["Successful Records"], row["Errored Records"]
        ),
        axis=1,
    )

    # Format Success Rate column as percentage
    df["Success Rate"] = df["Success Rate"].apply(lambda x: f"{x:.1f}%")

    # Reorder the columns
    df = df[["Date", "Name", "Successful Records", "Errored Records", "Success Rate"]]

    # Load existing data from Excel file
    try:
        existing_df = pd.read_excel("Day 91 Load Stats.xlsx")
        # Concatenate existing data with new data
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        # If the file does not exist, use only the new data
        combined_df = df

    # Save combined data to Excel file
    try:
        existing_df = pd.read_excel("Day 91 Load Stats.xlsx")
        # Concatenate existing data with new data
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        # Save combined data to the existing Excel file without overwriting
        combined_df.to_excel("Day 91 Load Stats.xlsx", index=False)
    except FileNotFoundError:
        # If the file does not exist, use only the new data
        df.to_excel("Day 91 Load Stats.xlsx", index=False)

    # Write DataFrame to a new Excel file
    date_str = datetime.date.today().strftime("%Y%m%d")
    file_name = f"Day91LoadStats-{date_str}.xlsx"
    df.to_excel(file_name, index=False)


if __name__ == "__main__":
    main()
