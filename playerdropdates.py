import pandas as pd

# Load your CSV file
df = pd.read_csv('draftresults.csv')

'''
Need to add value here for midpoint of season in weeks. Then calc drop dates based on that.
'''

# Step 2: Set the season start date for NFL season
season_start_date = pd.to_datetime('2023-09-07')

# Create a blank "Time Frame" column
df['Time Frame'] = None

# Sort the DataFrame by the "Round" column in ascending order
df.sort_values(by='Round', inplace=True)

# Determine the number of rows in the DataFrame
num_rows = len(df)

# Assign values in the "Time Frame" column
df.iloc[:2, df.columns.get_loc('Time Frame')] = 8  # Top 2 values are set to 7
df.iloc[-2:, df.columns.get_loc('Time Frame')] = 0  # Bottom 2 values are set to 1

# Calculate the number of remaining rows
remaining_rows = num_rows - 4

# Distribute values equally between 7 and 1 for the remaining rows in descending order
if remaining_rows > 0:
    step = 6 / remaining_rows
    df.iloc[2:-2, df.columns.get_loc('Time Frame')] = sorted([(i * step) + 1 for i in range(remaining_rows)], reverse=True)

# Convert the "Time Frame" column to integers
df['Time Frame'] = df['Time Frame'].astype(int)

# Step 4: Add values in the "Time Frame" column to Season Start Date variable
df['When To Drop'] = season_start_date + pd.to_timedelta(df['Time Frame'], unit='W')

# Display the updated dataframe
df.to_csv('dropdates.csv', index = False)
