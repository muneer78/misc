import numpy as np
import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_excel('RTSCS Regional Opportunity Upload - CHI 9.13.xlsx', sheet_name='TEMPLATE')

profile = ProfileReport(df, title="SAL 7135 Profile Report")

profile.to_file("SAL 7135 Open.html")

print("All Done")