import pandas as pd

df = pd.read_csv("tasks.csv")
df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)
df["Created Date"] = pd.to_datetime(df["Created Date"], infer_datetime_format=True)
df["Status"] = df["Status"].str.replace("Open", "Completed")
df.groupby("Activity ID").agg({"Activity ID": "count", "Created Date": "max"})
summary = df.sort_values(by=["Created Date"], ascending=False).drop_duplicates(
    ["Activity ID"]
)
tasksummary = df[["Activity ID", "Status"]]

# print(df)
print(tasksummary)

tasksummary.to_csv("taskstoclose.csv")
