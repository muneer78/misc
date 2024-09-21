import pyperclip

# Use if blank lines also need to be block quoted
def add_gt_in_front_of_paragraphs(text):
    # Split the text into lines
    lines = text.split('\n')

    # Add '> ' in front of each line, including blank lines
    updated_lines = [f'> {line}' if line.strip() else '> ' for line in lines]

    # Join the lines back with newline
    updated_text = '\n'.join(updated_lines)

    return updated_text

# Use if blank lines don't need to be block quoted
# def add_gt_in_front_of_paragraphs(text):
#     # Split the text into paragraphs based on double newline
#     paragraphs = text.split('\n\n')

#     # Add '> ' in front of each paragraph
#     updated_paragraphs = [f'> {paragraph.strip()}' for paragraph in paragraphs]

#     # Join the paragraphs back with double newline
#     updated_text = '\n\n'.join(updated_paragraphs)

    return updated_text

    # Join the lines back with newline
    updated_text = '\n'.join(updated_lines)

    return updated_text

# Sample input text
input_text = """
IIt has caused issues with my partner because, although he is incredibly understanding and patient, it eventually led to him feeling rejected and unloved and not initiating any more.

My tip has to be that you just have to make it a conscious thought to initiate. It doesn’t always have to lead to full on sexy time, it can be foreplay and just touchy stuff as well. Having conversations about your fantasies (it doesn’t have to be kinky it can literally just be fantasies of intercourse or kissing) really helped kind of make it easier for me to initiate. So if you have a day where you’re in a good mood and you think your partner is looking particularly nice, Maybe try to initiate something there? I’ve had to basically realise that I don’t get aroused unless we’re engaging in intimate time but a sign that I want to be intimate is when I look at my boyfriend and just admire how good he looks. So for me that admiration actually means I’m aroused but I’ve had to make that link myself because I never realised it before.

Overall though, you need to be having conversations with your partner. Like it will take multiple conversations, they won’t always be easy conversations and it has to be an ongoing effort from both of you.

The thing I would recommend the most is you need to do some reflection on why you can just exist without sexual intimacy. Sometimes the reason isn’t just as simple as out of sight out of mind. For me, I realised it had a lot to do with my past traumas and so I have almost become sex repulsed, although I’m not repulsed anymore since I’ve started trying to work on it.

Also, it’s possible you might not be feeling very romanced by your partner? At one point I realised my lack of sexual thought was tied to the fact that I felt my partner wasn’t attracted to me and I felt he wasn’t doing enough romantic things to make me feel very obviously desired. Like I knew he loves me but it felt like an afterthought because my love language is partially gifts and he had stopped buying me flowers etc. and he kept calling me cute instead of beautiful and so I felt very unattractive, as superficial as all of that may sound. So maybe there are some romantic things they could do to make you feel more desired.

But yeah my advice, summarised, would be: talk to your partner, reflect on why you feel the way you do, try and figure out if you have more subtle arousal cues and make that connection, and actively remind yourself to engage in some form of physical intimacy (again it doesnt have to be full on intercourse) every once in a while. Start slow and be patient with yourself, you can set a goal if you want of how often you would like to be intimate, if you do that start with a low goal first and build on it. I cannot stress enough the importance of discussing this with your partner though because they have to be actively working with you on this and supporting you or it will be harder for you to do.

Also, talking with your partner is very important to see what level of sexual intimacy they would be satisfied with. I was pressuring myself to engage in full on intercourse and making myself increasingly anxious until my boyfriend told me he would be very happy with just having foreplay with no full on sex involved. So knowing that can make things a whole lot easier because you can build on the smaller acts of sexual intimacy.
"""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
