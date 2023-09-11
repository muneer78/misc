import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_excel('pfj_day_91_scrub_output_202308291319.xlsx', sheet_name=['Create Lead', 'Create Opp', 'Create Opp - Exception'])
df_leads = df.get('Create Lead')
df_newopps = df.get('Create Opp')
# df_newoppserror = df.get('Create Opp - Exception')
df_reassignopps = df.get('Reassign Opp')

profile_leads = ProfileReport(df_leads, title="Leads Profiling Report")
profile_newopps = ProfileReport(df_newopps, title="New Opps Profiling Report")
# profile_newoppserror = ProfileReport(df_newoppserror, title="New Opps Exceptions Profiling Report")
profile_existingopps = ProfileReport(df_reassignopps, title="Reassign Ops Profiling Report")

profile_leads.to_file("Leads.html")
profile_newopps.to_file("New Opps.html")
# profile_newoppserror.to_file("New Opps Exceptions.html")
profile_existingopps.to_file("Reassigned Ops.html")