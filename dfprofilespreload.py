import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from ydata_profiling import ProfileReport

# Set the font family and size
plt.rcParams['font.family'] = 'Noto Sans'
plt.rcParams['font.size'] = 12

# Get today's date in the desired format (assuming YYYY-MM-DD)
today_date = datetime.today().strftime('%Y-%m-%d')

# Construct the filenames using f-strings
leads_filename = f'{today_date}-Day91Leads.csv'
newopps_filename = f'{today_date}-Day91NewOpps.csv'
reassignops_filename = f'{today_date}-Day91ReassignOpps.csv'

# Create a dictionary to store DataFrames for each CSV file
csv_files = {
    'Leads': leads_filename,
    'New Opps': newopps_filename,
    'Reassign Opps': reassignops_filename
}

# Create a PDF file to save the plots
pdf_filename = f'{today_date}-Day91RepAssignments.pdf'
pdf_pages = PdfPages(pdf_filename)

def create_bar_plot(title, counts):
    plt.figure(figsize=(10, 6))
    
    # Use sorted data for plotting
    sorted_counts = counts.sort_index(ascending=False)
    ax = sorted_counts.plot(kind='barh')  # Change to horizontal bar plot
    
    plt.title(title)
    plt.xlabel('Count')
    plt.ylabel('Rep Name')

    # Add total count next to each bar without .0
    for p in ax.patches:
        width = int(p.get_width())  # Convert the width to an integer
        ax.annotate(str(width), (p.get_width(), p.get_y() + p.get_height() / 2.), ha='left', va='center')

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    pdf_pages.savefig()  # Save the current plot to the PDF
    plt.close()  # Close the plot to free memory

# Load actual lead uploaded data
df_leads = pd.read_csv(leads_filename)
df_leads = df_leads.dropna(axis=1, how='all')
counts1 = df_leads['rep'].value_counts().sort_values(ascending=False)  # Sort in descending order
create_bar_plot('Rep Assignments for Leads', counts1)
profile_leads = ProfileReport(df_leads, title="Leads Profiling Report")


# Load new opportunities data
df_newopps = pd.read_csv(newopps_filename)
df_newopps = df_newopps.dropna(axis=1, how='all')
profile_newopps = ProfileReport(df_newopps, title="New Opps Profiling Report")
counts2 = df_newopps['rep'].value_counts().sort_values(ascending=False)  # Sort in descending order
create_bar_plot('Rep Assignments for New Opps', counts2)

# Load reassign opportunities data
df_reassignopps = pd.read_csv(reassignops_filename)
df_reassignopps = df_reassignopps.dropna(axis=1, how='all')
profile_reassignopps = ProfileReport(df_reassignopps, title="Reassign Ops Profiling Report")
counts3 = df_reassignopps['rep'].value_counts().sort_values(ascending=False)  # Sort in descending order
create_bar_plot('Rep Assignments for Reassigned Opps', counts3)

# Close the PDF file
pdf_pages.close()

# Create profile reports and save them to HTML files
for sheet_name, filename in csv_files.items():
    df = pd.read_csv(filename)  # Load the CSV file
    profile = ProfileReport(df, title=f"{sheet_name} Profiling Report")
    profile.to_file(f"{sheet_name.replace(' ', '_')}.html")

print("Charts are created")