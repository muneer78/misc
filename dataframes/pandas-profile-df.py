import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import missingno

# Set the font family and size
plt.rcParams["font.family"] = "Noto Sans"
plt.rcParams["font.size"] = 12

# Get today's date in the desired format (assuming YYYY-MM-DD)
today_date = datetime.today().strftime("%Y-%m-%d")

# Construct the filenames using f-strings
newopps_filename = f"{today_date}-Day91NewOpps.csv"
reassignops_filename = f"{today_date}-Day91ReassignOpps.csv"

# Create a PDF file to save the plots
pdf_filename = f"{today_date}-Day91RepAssignments.pdf"
pdf_pages = PdfPages(pdf_filename)

# Create the Excel writer filename using f-string
excel_filename = f"{today_date}-DataSummary.xlsx"
excel_writer = pd.ExcelWriter(excel_filename, engine="xlsxwriter")


def create_bar_plot(title, counts):
    plt.figure(figsize=(10, 6))

    # Use sorted data for plotting
    sorted_counts = counts.sort_index(ascending=False)
    ax = sorted_counts.plot(kind="barh")  # Change to horizontal bar plot

    plt.title(title)
    plt.xlabel("Count")
    plt.ylabel("Rep Name")

    # Add total count next to each bar without .0
    for p in ax.patches:
        width = int(p.get_width())  # Convert the width to an integer
        ax.annotate(
            str(width),
            (p.get_width(), p.get_y() + p.get_height() / 2.0),
            ha="left",
            va="center",
        )

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    pdf_pages.savefig()  # Save the current plot to the PDF
    plt.close()  # Close the plot to free memory


def generate_missing_data_plot(
    data_frame,
    record_type="",
    color="royalblue",
    sort="ascending",
    figsize=(10, 5),
    fontsize=12,
):
    today_date = datetime.now().strftime("%Y%m%d")

    fig = missingno.bar(
        data_frame, color=color, sort=sort, figsize=figsize, fontsize=fontsize
    )
    fig_filename = f"{today_date}-{record_type}MissingDataPlot.png"

    fig_copy = fig.get_figure()
    fig_copy.savefig(fig_filename, bbox_inches="tight")

    plt.close(fig_copy)


# Load actual lead uploaded data
success = pd.read_csv("success.csv")
success = success.dropna(axis=1, how="all")
counts1 = (
    success["REP"].value_counts().sort_values(ascending=False)
)  # Sort in descending order
create_bar_plot("Rep Assignments for Successfully Loaded Leads", counts1)
generate_missing_data_plot(success, record_type="Lead")


# Load new opportunities data
df_newopps = pd.read_csv(newopps_filename)
df_newopps = df_newopps.dropna(axis=1, how="all")
counts2 = (
    df_newopps["rep"].value_counts().sort_values(ascending=False)
)  # Sort in descending order
create_bar_plot("Rep Assignments for New Opps", counts2)
generate_missing_data_plot(df_newopps, record_type="NewOpps")

# Load reassign opportunities data
df_reassignops = pd.read_csv(reassignops_filename)
df_reassignops = df_reassignops.dropna(axis=1, how="all")
counts3 = (
    df_reassignops["rep"].value_counts().sort_values(ascending=False)
)  # Sort in descending order
create_bar_plot("Rep Assignments for Reassigned Opps", counts3)
generate_missing_data_plot(df_reassignops, record_type="ReassignOpps")

success.describe(include="all").to_excel(
    excel_writer, sheet_name="Successful_Leads_Summary"
)

df_newopps.describe(include="all").to_excel(excel_writer, sheet_name="NewOpps_Summary")

df_reassignops.describe(include="all").to_excel(
    excel_writer, sheet_name="ReassignOpps_Summary"
)

# Auto-format columns to fit content
worksheet_dict = excel_writer.sheets
for sheet_name, worksheet in worksheet_dict.items():
    for idx, col in enumerate(success.columns):
        max_len = max(success[col].astype(str).apply(len).max(), len(col))
        worksheet.set_column(idx, idx, max_len)  # Set column width to max_len

# Close the Excel writer
excel_writer.close()

# Close the PDF file
pdf_pages.close()
