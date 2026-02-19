"""
Using pandas to create dataframe
"""

import pandas as pd

# Create dataframe
df = pd.read_csv("books.csv")


def get_random_row(category):
    """
    Retrieve a random row from the dataframe based on the given category.

    Parameters:
    - category (str): The category to filter the dataframe by.

    Returns:
    - pandas.Series: A random row from the dataframe matching the category.
    """
    category_df = df[df["Tags"].astype(str).str.contains(category, na=False)]
    random_row_temp = category_df.sample()
    return random_row_temp


# Example usage
category_input = input("Enter a category: ")
random_row = get_random_row(category_input)
selected_columns = ["Title", "Primary Author", "Tags"]
print("The book to read next is")
print(random_row[selected_columns])
