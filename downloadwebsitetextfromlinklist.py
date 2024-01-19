import csv
import requests
from newspaper import Article

# Function to extract title and body text from a URL
def extract_title_and_body(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title, article.text

# Main function to process CSV and generate output
def process_csv(input_csv, output_text):
    urls = []

    with open(input_csv, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row:  # Check if the row is not empty
                urls.append(row[0])

    # Write each URL's title and body text to a text file
    with open(output_text, 'w', encoding='utf-8') as text_file:
        for i, url in enumerate(urls):
            title, body_text = extract_title_and_body(url)

            # Write page title to the top of the file
            text_file.write(f"Page Title: {title}\n\n")

            # Write body text
            text_file.write(body_text + '\n\n')

            # Add separator lines
            if i < len(urls) - 1:
                separator = '-' * 20
                text_file.write(separator + '\n\n')

# Example usage
process_csv('zitron.csv', 'zitron.txt')
