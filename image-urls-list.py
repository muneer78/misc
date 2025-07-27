import os
import re

def find_image_urls_in_markdown(folder_path):
    """
    Finds all standard Markdown image URLs in .md files within a given folder
    and its subfolders.

    Args:
        folder_path (str): The path to the folder to search.

    Returns:
        list: A list of unique image URLs found.
    """
    image_urls = set()  # Use a set to store unique URLs
    # Regex for standard Markdown image syntax: ![alt text](image_url)
    # It captures everything inside the parentheses for the URL.
    markdown_image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = markdown_image_pattern.findall(content)
                        for url in matches:
                            image_urls.add(url)
                except Exception as e:
                    print(f"Error reading file {filepath}: {e}")
    return sorted(list(image_urls)) # Convert to list and sort for consistent output

if __name__ == "__main__":
    # Get the folder path from user input
    folder_to_scan = input("Enter the path to the folder containing your Markdown posts: ")

    if not os.path.isdir(folder_to_scan):
        print(f"Error: The provided path '{folder_to_scan}' is not a valid directory.")
    else:
        print(f"\nSearching for image URLs in '{folder_to_scan}' and its subfolders...\n")
        found_urls = find_image_urls_in_markdown(folder_to_scan)

        if found_urls:
            print("Found Image URLs:")
            for url in found_urls:
                print(url)
        else:
            print("No Markdown image URLs found in the specified folder.")