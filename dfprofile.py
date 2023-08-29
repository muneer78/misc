import pandas as pd
from skimpy import skim
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Get today's date in the desired format (assuming YYYY-MM-DD)
today_date = datetime.today().strftime('%Y-%m-%d')

# # Construct the filenames using f-strings
newopps_filename = f'{today_date}-Day91NewOpps.csv'
reassignops_filename = f'{today_date}-Day91ReassignOpps.csv'

# Create a PDF file to save the plots
pdf_filename = f'{today_date}-Day91RepAssignments.pdf'
pdf_pages = PdfPages(pdf_filename)

def create_stacked_bar_plot(title, counts):
    plt.figure(figsize=(10, 6))
    ax = counts.plot(kind='bar', stacked=True)
    plt.title(title)
    plt.xlabel('Rep Name')
    plt.ylabel('Count')

    # Add total count above each bar without .0
    for p in ax.patches:
        height = int(p.get_height())  # Convert the height to an integer
        ax.annotate(str(height), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    pdf_pages.savefig()  # Save the current plot to the PDF
    plt.close()  # Close the plot to free memory

# Load actual lead uploaded data
success = pd.read_csv('success.csv')
success = success.dropna(axis=1, how='all')
skim(success)
counts4 = success['REP'].value_counts()
create_stacked_bar_plot('Rep Assignments for Successfully Loaded Leads', counts4)

# Load new opportunities data
df_newopps = pd.read_csv(newopps_filename)
df_newopps = df_newopps.dropna(axis=1, how='all')
skim(df_newopps)
counts2 = df_newopps['rep'].value_counts()
create_stacked_bar_plot('Rep Assignments for New Opps', counts2)

# Load reassign opportunities data
df_reassignops = pd.read_csv(reassignops_filename)
df_reassignops = df_reassignops.dropna(axis=1, how='all')
skim(df_reassignops)
counts3 = df_reassignops['rep'].value_counts()
create_stacked_bar_plot('Rep Assignments for Reassigned Opps', counts3)

# Close the PDF file
pdf_pages.close()
