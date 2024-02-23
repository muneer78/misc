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

    # Input data for three rows
    for _ in range(3):
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
    df["Success Rate"] = df["Success Rate"].apply(lambda x: f"{x:.0f}%")

    df.to_csv(f"Day91LoadStats-{date}.csv", index=False)


if __name__ == "__main__":
    main()
