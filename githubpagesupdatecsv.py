import pandas as pd
import re
from datetime import datetime

# Load the CSV file into a DataFrame
file_path = 'blog.csv'
df = pd.read_csv(file_path)

# Function to clean and format the Title column
def clean_title(title):
    # Remove special characters and change to lowercase
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title).strip().lower()
    # Replace spaces with dashes
    title = re.sub(r'\s+', '-', title)
    return title

# Apply the function to the Title column
df['Title'] = df['Title'].apply(clean_title)

# Function to reformat the Post date column
def reformat_date(date_str):
    # Convert the date from mm/dd/yy to yyyy-mm-dd
    date_obj = datetime.strptime(date_str, '%m/%d/%y')
    return date_obj.strftime('%Y-%m-%d')

# Apply the function to the Post date column
df['Post date'] = df['Post date'].apply(reformat_date)

# Save the modified DataFrame back to a CSV file
output_file_path = 'updated_file.csv'
df.to_csv(output_file_path, index=False)

print(f'Updated CSV file has been saved to {output_file_path}')
