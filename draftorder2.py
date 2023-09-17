"""
Use numpy to shuffle items
"""
import numpy as np
import pandas as pd

places = ["Britt", "Muneer", "Steven", "Scott", "Jason", "Lisa", "Carl", "Brian", "Nick", "Tony"]

# Initialize a dictionary to store the counts
counts = {place: 0 for place in places}

# Run the code 1000 times
for _ in range(1000):
    np.random.shuffle(places)
    first_place = places[0]
    counts[first_place] += 1

# Create a DataFrame from the counts dictionary
df = pd.DataFrame(list(counts.items()), columns=['Place', 'Count'])

# Sort the DataFrame in descending order by the Count column
df = df.sort_values(by='Count', ascending=False)

print(df)
