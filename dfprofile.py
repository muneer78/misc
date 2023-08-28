import pandas as pd
from skimpy import skim
from datetime import datetime

# Get today's date in the desired format (assuming YYYY-MM-DD)
today_date = datetime.today().strftime('%Y-%m-%d')

# # Construct the filenames using f-strings
leads_filename = f'{today_date}-Day91Leads.csv'
newopps_filename = f'{today_date}-Day91NewOpps.csv'
reassignops_filename = f'{today_date}-Day91ReassignOpps.csv'


# Load leads data
df_leads = pd.read_csv(leads_filename)

# Drop columns with all NA values
df_leads = df_leads.dropna(axis=1, how='all')

skim(df_leads)
counts1 = df_leads['rep'].value_counts()
print("Leads Value Counts:")
print(counts1)

# Load actual lead uploaded data
success = pd.read_csv('success.csv')

# Drop columns with all NA values
success = success.dropna(axis=1, how='all')

skim(success)
counts4 = success['REP'].value_counts()
print("Loaded Leads Value Counts:")
print(counts4)

# Load new opportunities data
df_newopps = pd.read_csv(newopps_filename)

# Drop columns with all NA values
df_newopps = df_newopps.dropna(axis=1, how='all')

skim(df_newopps)
counts2 = df_newopps['rep'].value_counts()
print("New Opportunities Value Counts:")
print(counts2)

# Load reassign opportunities data
df_reassignops = pd.read_csv(reassignops_filename)

# Drop columns with all NA values
df_reassignops = df_reassignops.dropna(axis=1, how='all')

skim(df_reassignops)
counts3 = df_reassignops['rep'].value_counts()
print("Reassign Opportunities Value Counts:")
print(counts3)
