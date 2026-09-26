import pandas as pd

df = pd.read_csv("DOTandMCExceptionsFile.csv")

# Assuming df is your DataFrame
df.sort_values(by=["dot_number__c", "UID"], inplace=True)

df.to_csv("DOTandMCExceptionsFile.csv", index=False)
