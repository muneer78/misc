import pandas as pd

df = pd.read_csv(r"/Users/muneer78/files/data/adult-follows.csv")

# Filter rows with both conditions
df_filtered = df[(df["reddit"] == "y") | (df["login-site"] == "reddit")]

df_filtered_sorted = df_filtered.sort_values(by=["account-name"])

output_file = r"/Users/muneer78/Downloads/reddit.csv"
df_filtered_sorted.to_csv(output_file, index=False)

print(df_filtered_sorted.head())
print(f"Filtered and sorted CSV written to {output_file}")