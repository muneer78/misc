import re

def convert_html_to_markdown(text):
    # Step 1: Replace <p> and </p> tags with line breaks
    text = re.sub(r'</?p>', '\n', text)

    # Step 2: Replace <img> tags with markdown image syntax
    text = re.sub(r'<img src="([^"]+)" alt="([^"]+)"[^>]*>', r'![\2](https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/\2)', text)

    # Step 3: Replace <hr> tags with horizontal rule
    text = re.sub(r'<hr>', '\n___\n', text)

    # Step 4: Remove empty <p></p> tags and excess newlines
    text = re.sub(r'\n{2,}', '\n\n', text)  # Reduces multiple newlines to a maximum of two
    text = re.sub(r'<p></p>', '', text)

    # Step 5: Replace blockquote <blockquote><p>...</p></blockquote> with markdown blockquote
    text = re.sub(r'<blockquote><p>(.*?)<\/p><\/blockquote>', r'> \1', text, flags=re.DOTALL)

    # Remove any remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    return text.strip()

html_text = '''
<p>First, I wish I could say this every day to at least one person:</p><p><img src="https://assets.buttondown.email/images/d4ca985e-3f5d-4caf-9bd8-f288339096f4.png?w=960&amp;fit=max"></p><hr><p>Second, anyone who has a significant other can relate to this. Men and women:</p><p><img src="https://assets.buttondown.email/images/6e1918b0-be9e-4885-90f2-6901836d038e.png?w=960&amp;fit=max"></p><hr><p>Third, this is the pun of the millenium:</p><p><img src="https://assets.buttondown.email/images/858b83ac-c0f8-4373-8e62-6448fe2dcdc8.png?w=960&amp;fit=max"></p><p></p>
'''

markdown_text = convert_html_to_markdown(html_text)
print(markdown_text)
