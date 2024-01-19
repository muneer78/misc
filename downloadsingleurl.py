from newspaper import Article

# Function to extract body text from a URL
def extract_body(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# Main function to process URL and print body text to terminal
def process_url(url):
    body_text = extract_body(url)

    if body_text:
        print(body_text)
    else:
        print("Failed to retrieve content from the provided URL.")

# Example usage
url_input = input("Enter the URL: ")
process_url(url_input)
