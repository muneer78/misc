import pandas as pd

# Sample data
df = pd.DataFrame(
    {"Category": ["A", "B", "A", "B", "A", "C"], "Value": [10, 20, 30, 15, 25, 5]}
)

# Define the criteria
criteria = "A"

# Perform SUMIF
sumif_result = df[df["Category"] == criteria]["Value"].sum()

# Display the result
print(f'SUMIF result for Category "{criteria}": {sumif_result}')
