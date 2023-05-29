import pandas as pd
import random

# Create dataframe
df = pd.read_csv('books.csv')

# Function to retrieve a random row based on category
def get_random_row(category):
    category_df = df[df['Tags'].astype(str).str.contains(category, na=False)]
    random_row = category_df.sample()
    return random_row

# Example usage
category_input = input("Enter a category: ")
random_row = get_random_row(category_input)
selected_columns = ['Title', 'Primary Author', 'Tags']
print("The book to read next is")
print(random_row[selected_columns])