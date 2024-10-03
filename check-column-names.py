import pandas as pd

player_list_df = pd.read_csv("Player List.csv")
rankings_df = pd.read_csv("laghezzaranks.csv")

print("Player List columns:", player_list_df.columns)
print("Rankings columns:", rankings_df.columns)