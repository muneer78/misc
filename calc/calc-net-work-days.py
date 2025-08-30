import numpy as np


def excel_networkdays(start_date, end_date, holidays=None):
    """
    Calculate the number of working days (excluding weekends and holidays) between two dates.

    Parameters:
    - start_date: Start date in the format 'YYYY-MM-DD'
    - end_date: End date in the format 'YYYY-MM-DD'
    - holidays: List of holiday dates in the format 'YYYY-MM-DD'

    Returns:
    - Number of working days
    """
    # Convert start and end dates to numpy datetime64 format
    start_date = np.datetime64(start_date)
    end_date = np.datetime64(end_date)

    # Convert holiday dates to numpy datetime64 format (if provided)
    if holidays:
        holidays = np.array([np.datetime64(h) for h in holidays])

    # Calculate the number of working days using numpy.busday_count
    num_working_days = np.busday_count(start_date, end_date, holidays=holidays)

    return num_working_days


# Example usage:
start_date = "2024-01-01"
end_date = "2024-01-31"
holidays = ["2024-01-10", "2024-01-17"]

result = excel_networkdays(start_date, end_date, holidays)
print(f"Number of working days: {result}")
