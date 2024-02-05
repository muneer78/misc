import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv('BIR-10010 MC Auth 202309131411.csv')
# Drop rows where 'carrier_authority_date' is blank or null
df = df.dropna(subset=['carrier_authority_date'])

profile = ProfileReport(df, title="SAL 7128 Profile Report")

profile.to_file("SAL 7128.html")

print("All Done")