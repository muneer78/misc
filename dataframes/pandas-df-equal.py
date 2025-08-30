import pandas as pd

# create two dataframes with different shapes and column names
df1 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
df2 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 7], "C": [10, 11, 12]})

# Comparing Dataframes with the Same Shape and Column Names
print(df1.equals(df2))  # True

# compare dataframes
diff = df1.compare(df2)

# print differences
print(diff)
