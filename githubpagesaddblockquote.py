import pyperclip

def add_gt_in_front_of_paragraphs(text):
    # Split the text into paragraphs based on double newline
    paragraphs = text.split('\n\n')

    # Add '> ' in front of each paragraph
    updated_paragraphs = [f'> {paragraph.strip()}' for paragraph in paragraphs]

    # Join the paragraphs back with double newline
    updated_text = '\n\n'.join(updated_paragraphs)

    return updated_text

# Sample input text
input_text = """I was at a shitty crustpunk bar once getting an after-work beer. One of those shitholes where the bartenders clearly hate you. So the bartender and I were ignoring one another when someone sits next to me and he immediately says, "no. get out."

And the dude next to me says, "hey i'm not doing anything, i'm a paying customer." and the bartender reaches under the counter for a bat or something and says, "out. now." and the dude leaves, kind of yelling. And he was dressed in a punk uniform, I noticed

Anyway, I asked what that was about and the bartender was like, "you didn't see his vest but it was all nazi shit. Iron crosses and stuff. You get to recognize them."

And i was like, ohok and he continues.

"you have to nip it in the bud immediately. These guys come in and it's always a nice, polite one. And you serve them because you don't want to cause a scene. And then they become a regular and after awhile they bring a friend. And that dude is cool too.

And then THEY bring friends and the friends bring friends and they stop being cool and then you realize, oh shit, this is a Nazi bar now. And it's too late because they're entrenched and if you try to kick them out, they cause a PROBLEM. So you have to shut them down.

And i was like, 'oh damn.' and he said "yeah, you have to ignore their reasonable arguments because their end goal is to be terrible, awful people."

And then he went back to ignoring me. But I haven't forgotten that at all."""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
