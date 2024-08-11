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
<img src="https://buttondown-attachments.s3.amazonaws.com/images/f8203f71-6737-4685-8451-9e296029f375.png" alt="madness.png" />
<hr>
<p>Ever since I saw this, I can never stop laughing when I see it:</p>
<img src="https://buttondown-attachments.s3.amazonaws.com/images/be0c25b5-7788-44af-9be8-823ab8460723.png" alt="VodkaPapaJohns.png" />
<hr>
<p><a href="https://www.reddit.com/r/worldnews/comments/4oiz4f/exauschwitz_guard_reinhold_hanning_94_sentenced/d4dkbu2">This Reddit post</a> about Adolf Eichmann has some very deep insights about why people choose to believe in things like conspiracy theories:</p>
<blockquote>
<p>In a search for some higher meaning, he gave himself to a cause so completely that he was unable to think outside of it&#39;s cliche&#39;s, standard lines... or from the point of view of other people. By adopting a cause Eichmann created a intellectual fence around himself and relieved himself of having to think critically or examine his convictions.</p>
</blockquote>
<hr>
<blockquote>
<p>There is pleasure in understanding the world around us and meaning in the unending work of developing and refining a coherent world view. Adopting an ideology, short circuits that effort, providing pleasure and meaning with an unwarranted (and unquestioned) degree of certainty. Consequently, fully adopting an ideology, whether it&#39;s Nazism or Feminism, is fundamentally not a benign act. People do this on a regular basis: unquestioned, mild, allegiance to their church, to their political party, to traditional values, to their social causes, etc. This is the essence of &quot;the banality of evil&quot; that Arendt talks about. There is a strong intellectual resemblance between the unquestioned beliefs and unexamined assumptions that allow a man to ship millions of people to extermination camps, and the unquestioned assumptions and beliefs that we all operate on, on a daily basis. Psychopathic cruelty and blood-thirst are not required.</p>
</blockquote>
---
'''

markdown_text = convert_html_to_markdown(html_text)
print(markdown_text)
