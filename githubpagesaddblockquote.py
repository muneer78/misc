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
input_text = """_(I work with a pair of identical twins for the overstock night shift. They know I’m atheist, so they’ve made it their business to preach their religion at me non-stop.)_

**Twin #1:** “So, [my name], you think about what we said on Tuesday?”

**Me:** “Not really.”

**Twin #1:** “Come on, man. This is important stuff.”

**Twin #2:** “Yeah. You wanna go to h***?”

**Me:** “Nope.”

**Twin #1:** “I mean, I just don’t get you.”

**Me:** “What do you mean?”

**Twin #1:** “If you don’t believe in God, where do you get your morals from?”

**Me:** “Uh…”

**Twin #2:** “Yeah. The only way to know right from wrong is with God.”

**Me:** “I don’t think so.”

**Twin #1:** “Well, it’s still true, dude. It doesn’t matter what you think.”

**Twin #2:** “Right. You should… hang on.”

_(Twin #2 gets a call on his cell phone and answers it. He turns away from his brother and me but keeps standing there.)_

**Twin #1:** “[My name], dude, do you think murder and rape are okay?”

**Me:** “No.”

**Twin #1:** “Well, that’s God, man. The only way you know that stuff is not okay is God.”

**Twin #2:** _*on the phone*_ “…You picked up my bike okay? No problems getting it? Cool…”

**Twin #1:** “How about lying? Or stealing? You think it’s okay to do that?”

**Me:** “No.”

**Twin #2:** _*on the phone*_ “..You think you could roll back the odometer about 5,000 miles…”

**Twin #1:** “Well, it was God who said lying and stealing are wrong, man. It’s right there in the Bible.”

**Twin #2:** _*on the phone*_ “…Yeah, I know. But I’ve got somebody coming out to look at it and he said he didn’t want it if it was too used…”

**Twin #1:** “So you KNOW that stuff like killing and raping and lying and stealing and being a racist and all that stuff is wrong. How do you explain how that’s wrong without God?”

**Twin #2:** _*on the phone*_ “…Oh yeah, you think you could paint over the rust on the brakes and the engine block, too? I’m pretty sure I could get at least two grand more out of this guy…”

**Twin #1:** “God is righteous, [my name]. He’s going to punish people for doing all that stuff. You don’t want to go to Hell, do you?”

**Twin #2:** _*on the phone*_ “…Also, I think the front tire has a hole in it. No, no, don’t patch it. Just put more air in it. It only has to look full until the guy buys it…”

**Me:** “Wait, wait, wait. Are you guys listening to each other here?”

**Both Twins:** “What do you mean?”"""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
