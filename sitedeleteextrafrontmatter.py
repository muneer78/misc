import os

def remove_second_text_block(text):
  """Removes the second text block from the given text.

  Args:
    text: The input text.

  Returns:
    The text with the second text block removed.
  """

  delimiter = "---\ntags: jokes\n---"
  lines = text.splitlines()
  found_first_delimiter = False
  new_lines = []
  for line in lines:
    if line.strip() == delimiter:
      found_first_delimiter = not found_first_delimiter
    if not found_first_delimiter:
      new_lines.append(line)
  return "\n".join(new_lines)

def process_directory(directory):
  """Processes all .md files in a given directory, removing the second text block.

  Args:
    directory: The path to the directory.
  """

  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith(".md"):
        file_path = os.path.join(root, file)
        try:
          with open(file_path, 'r') as f:
            text = f.read()
          new_text = remove_second_text_block(text)
          with open(file_path, 'w') as f:
            f.write(new_text)
        except Exception as e:
          print(f"Error processing file {file_path}: {e}")

# Example usage:
directory_to_process = "/Users/muneer78/Desktop/saved/"
process_directory(directory_to_process)
