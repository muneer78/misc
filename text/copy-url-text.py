from bs4 import BeautifulSoup
import requests
import pyperclip  # Library for clipboard operations

# Input: URL to fetch
url = input("Enter the URL: ").strip()

try:
    # Fetch the HTML content of the URL using requests
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the main body text (all paragraphs)
    paragraphs = soup.find_all("p")
    body_text = "\n".join(
        p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
    )

    # Copy the extracted text to the clipboard
    pyperclip.copy(body_text)

    # Count the number of characters in the extracted text
    char_count = len(body_text)

    # Output message
    print(
        f"The extracted text has been copied to the clipboard. (Character count: {char_count})"
    )

except requests.exceptions.RequestException as e:
    print(f"Error fetching {url}: {e}")
except Exception as e:
    print(f"Error processing {url}: {e}")
