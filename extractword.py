import pandas as pd

# Sample DataFrame
data = {"Text": ["Hello World", "Python is great", "Data Science"]}
df = pd.DataFrame(data)

# Extract the last word from the 'Text' column
df["Last_Word"] = df["Text"].str.split().str[-1]

# Display the result
print(df)
