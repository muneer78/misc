import pyperclip

def add_gt_in_front_of_paragraphs(text):
    # Split the text into lines
    lines = text.split('\n')

    # Add '> ' in front of each line, including blank lines
    updated_lines = [f'> {line}' if line.strip() else '> ' for line in lines]

    # Join the lines back with newline
    updated_text = '\n'.join(updated_lines)

    return updated_text

# Sample input text
input_text = """
What are facts?

There are many interpretations. Some of them say that facts are fluid and open to interpretation. Others say that only knowledge that is iron clad can be called a fact. The answet, to some, may lay in the middle. I dispute that interpretation. A fact is an incontrovertible truth. Everything else is opinion.

Journalism today has a lot of opinions masquerading as fact. We see headlines like, "Trump Keeps Proving He's Dumb" or "Hillary Was Even More Crooked Than We Thought". These types of headlines are from opinion factories masquerading as journalistic outlets. Info Wars, as an example, presents a lot of opinion and unproven conspiracy theories as if they were fact. They have poorly sourced articles claiming great malfeasance on the part of government with a minimum of support. Yet people still read that site and consider the content produced by it as if it were hard fact. 

The decline in thinking ability in this country is partially to blame. We have people who think that because they can Google something, they are suddenly on par with the experts in fields. People think that they know more than scholars who have devoted their whole lives to the study of a field. Sites like Info Wars encourage this kind of thinking because it serves their purposes. People who doubt facts can be duped into believing anything.
"""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
