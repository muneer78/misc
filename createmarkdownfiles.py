import os
from datetime import datetime, timedelta

def create_markdown_file(category, title, imagename, date):
    # Format title for filename
    filename_title = '-'.join(title.lower().split())

    # Create filename with date and formatted title
    filename = f"{date.strftime('%Y-%m-%d')}-{filename_title}.md"

    # Create content with the specified pattern
    content = f"""---
categories: {category}
title: {title}
---

![{imagename}](https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/{imagename}.jpg)
"""

    # Write content to the markdown file
    with open(filename, 'w') as file:
        file.write(content)

    print(f"Markdown file '{filename}' created successfully.")

# Example usage
tuples = [
    ("funny, black", "Black Dudes", "blackdudes.png"),
    ("funny", "Miette", "Miette-all.jpg"),
    ("funny", "Deep Magic", "deepmagic.png"),
    ("politics", "Make Fun of Fascists", "fascists.png"),
    ("funny", "Tooth Fairy", "bonesyouth.png"),
    ("memes", "Professor Gorilla", "gorillaprof.png"),
    ("work", "Performance Evaluations", "perfevals.png"),
    ("memes", "Mamaw", "mamaw.jpg"),
    ("funny", "Mascot", "mascots.jpg"),
    ("funny", "What I Really Said", "motherf.jpg"),
    ("memes", "Orca Song", "orca.jpg"),
    ("funny", "Memphis Cat", "paulwall.jpeg"),
    ("funny, work", "Awkward At Work", "worktrauma.jpg"),
]

# Start date
start_date = datetime(2024, 5, 1)

for i, (category, title, imagename) in enumerate(tuples):
    current_date = start_date + timedelta(days=i)
    create_markdown_file(category, title, imagename, current_date)
