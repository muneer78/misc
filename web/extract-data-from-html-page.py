import requests
from bs4 import BeautifulSoup

def get_nfl_strength_of_schedule():
    """
    Extracts the NFL Strength of Schedule data from a CBS Sports webpage.
    """
    url = "https://www.cbssports.com/nfl/news/2025-nfl-strength-of-schedule-for-all-32-teams-giants-bears-facing-rough-slates-49ers-have-it-easiest/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Fetching data from the webpage...")

    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the data. We'll look for a table with a specific
        # class or a header that indicates it's the right one.
        table = soup.find('table')

        if not table:
            print("Error: Could not find the table on the page.")
            return []

        # Find all table rows
        rows = table.find_all('tr')
        if not rows:
            print("Error: Could not find any rows in the table.")
            return []

        # Extract the header row
        headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]
        print(f"Scraped Headers: {headers}")

        # Extract data rows
        schedule_data = []
        for row in rows[1:]:  # Start from the second row to skip the header
            cells = row.find_all('td')
            if cells:
                row_data = [cell.get_text(strip=True) for cell in cells]
                # Create a dictionary for each team using the headers
                team_data = {headers[i]: row_data[i] for i in range(len(headers))}
                schedule_data.append(team_data)

        return schedule_data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == "__main__":
    nfl_schedule = get_nfl_strength_of_schedule()
    if nfl_schedule:
        print("\nSuccessfully extracted NFL Strength of Schedule data:")
        for team in nfl_schedule:
            # Print all key-value pairs in the dictionary to avoid KeyError
            print(', '.join([f"{key}: {value}" for key, value in team.items()]))
    else:
        print("Failed to extract data.")
