# import os
# import re
#
# def update_markdown_files(directory='.'):
#     Define the regular expressions to capture the patterns
#     pattern1 = r'!\[(.*?)\]\[(.*?)\]'
#     pattern2 = r'\[(.*?)\]: /sites/default/files/(.*?\.(?:jpeg|jpg|png|gif|svg|bmp|tiff|webp))'
#     replacement_base_url = 'https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/'
#     comment_pattern = r'<!-- Images -->'
#
#     # Iterate over all files in the given directory
#     for filename in os.listdir(directory):
#         if filename.endswith('.md'):
#             filepath = os.path.join(directory, filename)
#
#             # Read the content of the file
#             with open(filepath, 'r', encoding='utf-8') as file:
#                 content = file.read()
#
#             # Remove the comment text
#             content = re.sub(comment_pattern, '', content)
#
#             # Search for the patterns
#             match1 = re.search(pattern1, content)
#             match2 = re.search(pattern2, content)
#
#             if match1 and match2:
#                 alt_text = match1.group(1)
#                 reference = match1.group(2)
#                 file_extension = match2.group(2).split('.')[-1]
#
#                 # Construct the new replacement pattern
#                 new_pattern1 = f'![{alt_text}]({replacement_base_url}{match2.group(2)})'
#
#                 # Perform the replacement
#                 new_content = re.sub(pattern1, new_pattern1, content)
#                 new_content = re.sub(pattern2, '', new_content)
#
#                 # Extract text between the two patterns and move it to the end
#                 text_between_patterns = re.search(rf'{re.escape(match1.group(0))}(.*?){re.escape(match2.group(0))}', content, re.DOTALL)
#                 if text_between_patterns:
#                     text_between = text_between_patterns.group(1)
#                     new_content = new_content.replace(text_between, '') + text_between
#
#                 # Write the modified content back to the file
#                 with open(filepath, 'w', encoding='utf-8') as file:
#                     file.write(new_content)
#
# if __name__ == "__main__":
#     update_markdown_files()

import os
import re

def update_markdown_files(directory):
    # Define the pattern to search for "categories"
    categories_pattern = re.compile(r".*", re.IGNORECASE)

    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            filepath = os.path.join(directory, filename)

            # Read the content of the file
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace "categories" with "tags"
            updated_content = re.sub(categories_pattern, '', content)

            # Write the modified content back to the file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(updated_content)

if __name__ == "__main__":
    directory = '/Users/muneer78/Downloads/rename'  # Set your specific directory here
    update_markdown_files(directory)

