import pandas as pd
from datetime import datetime as dt

# Get the current date
current_date = dt.now()


# Function to create the cell colors based on the DataFrame and a specific column
def create_cell_colors(df, column_name):
    cell_colors = []
    for _, row in df.iterrows():
        try:
            value = float(row[column_name])  # Convert value to float for comparison
        except ValueError:
            value = None  # Handle non-numeric values gracefully

        if value is not None:
            if value > 50:
                cell_colors.append(["#FF9999"] * len(row))
            elif value < 20:
                cell_colors.append(["#99FF99"] * len(row))
            elif 20 <= value <= 50:
                cell_colors.append(
                    ["#FFFF99"] * len(row)
                )  # Yellow color for values between 20 and 50
            else:
                cell_colors.append(["#FFFFFF"] * len(row))
        else:
            cell_colors.append(
                ["#FFFFFF"] * len(row)
            )  # Default color for non-numeric values
    return cell_colors


# Function to apply pandas styling and save to Excel
def apply_excel_conditional_formatting(df, excel_output_path, column_name):
    def highlight(row):
        colors = []
        try:
            value = float(row[column_name])
        except ValueError:
            value = None

        if value is not None:
            if value > 50:
                colors = ["background-color: #FF9999"] * len(row)
            elif value < 20:
                colors = ["background-color: #99FF99"] * len(row)
            elif 20 <= value <= 50:
                colors = ["background-color: #FFFF99"] * len(row)
            else:
                colors = ["background-color: #FFFFFF"] * len(row)
        else:
            colors = ["background-color: #FFFFFF"] * len(row)

        return colors

    styled_df = df.style.apply(highlight, axis=1)
    styled_df.to_excel(excel_output_path, engine="openpyxl", index=False)


# Main function to run the entire process
def main(csv_file_path, excel_output_path, column_name):
    # Load DataFrame
    df = pd.read_csv(csv_file_path)

    # Apply Excel conditional formatting using pandas styling
    apply_excel_conditional_formatting(df, excel_output_path, column_name)


# Replace with your file paths
# Create the output filenames using f-strings

ticket_number = "insert Jira number here"
column_name = "fmcsa_trucks"
csv_file_path = "2024-05-29-Day91Leads.csv"
excel_output_path = f"DS{ticket_number}_{current_date}_output.xlsx"

# Run the main function
main(csv_file_path, excel_output_path, column_name)
