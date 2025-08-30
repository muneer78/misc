from datetime import datetime

def calculate_hours_elapsed(input_time_str):
    # Get the current time
    current_time = datetime.now()

    # Parse the input time
    input_time = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M:%S")

    # Calculate the number of hours elapsed
    elapsed_time = current_time - input_time
    elapsed_hours = elapsed_time.total_seconds() / 3600

    return elapsed_hours

# Example usage
input_time_str = "2025-01-03 15:00:00"
elapsed_hours = calculate_hours_elapsed(input_time_str)
print(f"Number of hours elapsed: {elapsed_hours:.2f}")