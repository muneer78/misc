def analyze_text_file(file_path):
    with open(file_path, "r") as file:
        text = file.read()

    # Number of characters
    num_characters = len(text)

    # Number of words
    words = text.split()
    num_words = len(words)

    # Number of pages
    words_per_page = 250
    num_pages = num_words / words_per_page

    return num_characters, num_words, num_pages


# Example usage
file_path = "/Users/muneer78/Downloads/abusiveparentsextended.txt"  # Replace with the path to your text file
characters, words, pages = analyze_text_file(file_path)
print(f"Number of characters: {characters}")
print(f"Number of words: {words}")
print(f"Number of pages: {pages:.2f}")
