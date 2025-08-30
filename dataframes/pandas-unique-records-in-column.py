import pandas as pd

df_leads = pd.read_csv("2023-09-06-Day91Leads.csv")
df_newopps = pd.read_csv("2023-09-06-Day91NewOpps.csv")

print("Leads DF Info:")
df_leads.info()

print("\n")
print("New Opps DF Info:")
df_newopps.info()

df_leads_unique = df_leads.nunique(axis=0, dropna=True)
df_newopps_unique = df_newopps.nunique(axis=0, dropna=True)

print("\n")

print("The number of unique values in the leads DF columns is as follows:")
print(df_leads_unique)
print("\n")
print("The number of unique values in the new opps DF columns is as follows:")
print(df_newopps_unique)
