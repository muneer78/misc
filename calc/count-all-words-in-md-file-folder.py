import os

def count_words_in_markdown(filepath):
  """Counts the number of words in a markdown file.

  Args:
    filepath: Path to the markdown file.

  Returns:
    The number of words in the file.
  """
  with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
  \# Simple word counting by splitting on whitespace
  words = content.split()
  return len(words)

def count_words_in_directory(directory):
  """Counts the total number of words in all markdown files within a directory.

  Args:
    directory: Path to the directory containing markdown files.

  Returns:
    The total word count across all markdown files.
  """
  total_words = 0
  for filename in os.listdir(directory):
    if filename.endswith(".md"):
      filepath = os.path.join(directory, filename)
      total_words += count_words_in_markdown(filepath)
  return total_words

if __name__ == "__main__":
  directory_to_search = "PUT THE PATH TO A FOLDER HERE"  \# Replace with your directory
  total_word_count = count_words_in_directory(directory_to_search)
  print(f"Total words in markdown files: {total_word_count}")