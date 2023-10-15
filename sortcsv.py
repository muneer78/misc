import pandas as pd

# Read CSV file into pandas dataframe
df = pd.read_csv('futures.csv')

# Convert date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Sort dataframe by date in ascending order
df.sort_values(by='Date', ascending=True, inplace=True)

# Save sorted dataframe back to CSV file
df.to_csv('futures.csv', index=False)