import pandas as pd
import matplotlib.pyplot as plt


# Step 1: Import CSV as DataFrame
def load_csv(file_path):
    return pd.read_csv(file_path)


# Step 2: Apply Conditional Formatting and Export to PDF
def apply_pdf_conditional_formatting(df, filename):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, len(df) * 0.5))

    # Define colors based on 'RankDiff' column
    cell_colors = []
    for index, row in df.iterrows():
        if pd.notnull(row["RankDiff"]):
            if row["RankDiff"] > 20:
                cell_colors.append(["#FF9999"] * len(row))
            elif row["RankDiff"] < -20:
                cell_colors.append(["#99FF99"] * len(row))
            else:
                cell_colors.append(["#FFFFFF"] * len(row))
        else:
            cell_colors.append(["#FFFFFF"] * len(row))

    # Create the table with colored cells
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
        cellColours=cell_colors,
    )

    # Remove axis
    ax.axis("off")

    # Save figure as PDF
    plt.savefig(filename, bbox_inches="tight")


# Main function to integrate all steps
def main(csv_file_path, pdf_output_path):
    # Load CSV
    df = load_csv(csv_file_path)

    # Apply conditional formatting and save to PDF
    apply_pdf_conditional_formatting(df, pdf_output_path)


# Replace with your file paths
csv_file_path = "draftsheet.csv"
pdf_output_path = "draftsheet.pdf"

# Run the main function
main(csv_file_path, pdf_output_path)
