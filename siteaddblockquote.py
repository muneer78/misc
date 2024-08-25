# import pyperclip
#
# def add_gt_in_front_of_paragraphs(text):
#     # Split the text into lines
#     lines = text.split('\n')
#
#     # Add '> ' in front of each line, including blank lines
#     updated_lines = [f'> {line}' for line in lines]
#
#     # Join the lines back with newline
#     updated_text = '\n'.join(updated_lines)
#
#     return updated_text
#
# # Sample input text
# input_text = """E> So my daughter is in a sorority, which I 100% supported. My wife and I paid for her dues and supported her when when she asked if we would be okay with it. Unfortunately, last week I found out something very upsetting. My daughter was trying to enroll for classes but had holds on her account with prevented her from doing so.
#
# > She called the university to get everything sorted out. When I asked her what happened she told me her sorority was in hot water for underaged drinking and they all had to take an online course about alcohol and student conduct on campus. When I asked why she didn’t tell me this before she told me she was too embarrassed to. I don’t know why (call it intuition I guess) but I didn’t believe her. I decided to do some research on my own and stumbled across an article written by her schools newspaper about a halloween party thrown by her sorority and their brother frat.
#
# > Since this isn’t a debate sub, I don’t want to say exact details but I will say the theming of the party was very offensive. In the article was a screenshot of an instagram post from the party and there I saw it, a picture of my daughter in a racially insensitive costume. When I confronted her about this she immediately became frustrated and told me it’s not that big of a deal and she didn’t tell me because she knew I’d blow it out of proportion.
#
# > I decided to leave the room and go talk to my wife about the situation before I said something I’d regret and my wife and I both decided that we will no longer pay for her sorority dues. Both my wife and I support racial equality and have always taught those morals to our daughter, to see her disregard them was very upsetting and we decided that we would not support our daughter in an environment which undermined those views. When we told her this she completely blew up, saying that we promised to pay for it etc. etc. She also called us financially abusive as we both know that she would not be able to pay for the dues herself and finding a job is nearly impossible.
#
# > She has one last payment due this semester and she doesn’t have the money to pay for it. She talked to her sisters and they told her that they would be willing to give her an extension until the fall semester, but she is unsure if she will have the money then. Our daughter is very upset with us and thinks we’re overreacting. She’s been crying for a week and I have to wonder, AITA for refusing to pay? Was our punishment too harsh?
#
# > EDIT1: Since everyone’s asking I guess I should state what the costume/theming was. The theme was “Pimps and hoes” (and those parties never go well.) And my daughter got box braids as well as an extremely deep tan, she’s extremely pale and while she does use spray tans I’ve never seen her this dark before. Think going from this to this. To me it was obviously emulating and making fun of black people which is extremely gross. I raised her better than that and I don’t know why she thought it would be okay.
#
# > EDIT2: I figured I would clear up some other misconceptions. First, my daughter didn’t have to take an alcohol class, she made that up. In reality she had to take a class pertaining to racial sensitivity/diversity and take a quiz afterwards. This course took her an hour tops. There was also a community service aspect but that was cancelled because school let out early. She was not the only student in an offensive costume, in the photo that was posted in the newspaper there were two other students in blackface as well. I do have to thank you all for your support and advice.Their dad is doing well now, those kids don't want for anything. Every Sunday night, he hosts us to watch football and hang out with the kids. His daughter delights in serving everyone "wheat juice." Their so much better of without this witch.
# """
#
# # Apply the function to the input text
# output_text = add_gt_in_front_of_paragraphs(input_text)
#
# # Copy the updated text to the clipboard
# pyperclip.copy(output_text)
#
# print("The updated text has been copied to the clipboard.")

import pyperclip

def add_gt_to_blank_lines(text):
    # Split the text into lines
    lines = text.split('\n')

    # Add '> ' only to blank lines
    updated_lines = [f'> ' if line.strip() == '' else line for line in lines]

    # Join the lines back with newline
    updated_text = '\n'.join(updated_lines)

    return updated_text

# Sample input text
input_text = """
---
date: 2024-07-14
title: Starbucks Fan Fic 
tags: stories, tumblr
---

[This](https://katjohnadams.tumblr.com/post/171462690508/katjohnadams-anais-ninja-blog) is such a great story:

> Actual conversation I had at register:

> “Hi, welcome to Starbucks! What can I get you, today?”

> “Oh. uh. Well, it’d be I suppose… I only have a button for a Quad. I don’t have special pricing for twenty ounces of espresso in a single… drink.”

> “Price is the furthest thing from my mind right now. How many ‘add shots’ is that?”

> *deep breath of fear* “It’d be a quad with,” *clears throat* “uh, sixteen additional shots of espresso. But, ma’am, I should tell you that the shots will start to get really bitter if they have to sit and wait for us to pull twenty of them-”

> “Taste means nothing to me.”

> At this point I am truly fearing for my very existence in the presence of what must clearly be an eldritch being.

> “Oh. Well, okay.” I put on my absolute best customer service smile to hide my terror and accept that I must face this dragon, fae, or demon with dignity. “We can certainly get that for you! The price will be _____.”

> She begins to pay, I shit thee not, with golden dollar coins. We are a block from Wall Street, and this eldritch demi-being is paying for an unholy elixer with golden coins. My life will end soon, I am sure of it.

> “Do you still have the ‘Add Energy’ packets?”

> My heart began to race at this request. “Yes ma’am.”

> “How many can I add?”

> Futile though it is, at least I know the rote response to this. “For health reasons, we won’t add more than one per drink and we cannot sell the packets individually.”

> “One then.”

> I alter the order and tell her the new price. She pays, dumps the change and five golden dollars into the tip box. I write the order on the venti cup and pass it silently to the girl working the hot beverage station. Normally we called and pass, but this was … not something to be spoken aloud.

> My fellow takes the cup, not thinking anything of the minor break with protocol, until she sees the order. She stares at me. “No.”

> The woman, which I call her for no other greater insight into her terrifying being is within my grasp, simply stands on the other side and says, calmly but with a commanding tone I expect of Admirals in bad movies, “Yes.”

> My fellow barista pales before her task. But we are dutiful, we are true to our task, great though it may be. She sets about clearing the two brand new Matrena’s of all distraction, and sets two tall cups in the ready position. The energy packet is emptied into the venti cup, and the shots begin pouring. 

> The barista was damn near shaking. This woman’s gaze felt like the fires of the sun. Finally, the shots are pulled, the cup is filled, and the hand off takes place.

> Our visiting Incomprehensible takes it to our milk bar and adds a dollop of cream. Satisfied, she proceeds to down what must have been half the damn cup.

> Then she smiled at us, like a benediction and I was honestly filled with joy. And horror. She left, and we knew nothing more of her after that.

> When I talk with other former employees, we quickly begin talking about “The Company” as if we’d never left, perhaps knowing that part of our soul still powers that awesome and terrible corporate machine. And when I share this story, other Baristas at first act shocked but quickly settle and comes the chorus, 

> “Yeah, I had one like that.”
"""

# Apply the function to the input text
output_text = add_gt_to_blank_lines(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
