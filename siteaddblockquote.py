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
input_text = """I hate “we’re fucked.”

I mean, I don’t want to shame anyone who has said it, thought it, or posted it. I have too. But as a philosophy, as a statement of belief, I hate it. Because it means you’ve given up. 

We are absolutely NOT fucked.

Things are so bad. This country has taken a turn that I could never have predicted. It is absolutely fascist, nativist, and extremist. It’s every bit as scary as it seems.

But we are not fucked.

I read a long-form article on the Russia hacks in the New Yorker not long ago. However much you think that influenced the outcome, it was an instructive piece of journalism. There is very little indication that there was a specific political agenda that was being wished for. The goal was simple: Sow chaos and undermine the faith of Westerners in their own institutions.

This is really important to think about right now.

I have a high regard for Mueller and I think his investigation will have some influence. But don’t wait on him to save us. He can’t. And don’t wait on impeachment. I would support it fervently, but it is nothing to bank on. And especially don't assume Trump can't win again. He absolutely can. Our best bet - better, even, than all of our protests and actions - is actually voting.

It’s so square. It’s so old-fashioned. Many of us involved with the hard-left or anarchist scene have been trained to disregard it.

Fucking don’t. NOT NOW, guys. It is the best tool at our disposal. Yeah, you can say that they will sabotage it, reject it, whatever. “Sufficient to the day is the evil thereof.” In other words, don’t create troubles before they exist. Anything seems possible to me right now, but it remains the case - despite hacked voting machines and gerrymandering - that there is no known mechanism by which our government can deny massive voter turnout.

Take back the House in November. Then take back the Presidency in 2020. The worst thing we could do is pretend that these are givens. I never, ever, ever thought that this piece of shit could sit in the Oval Office. I was so humbled by my error. Therefore I assume he could take it again - I know he could - unless we accept the threat as real.

When we say, “We’re fucked,” we roll over. We defeat ourselves. We do their job for them. Don’t do that. We are NOT fucked. We are in a fight. It sucks. It’s hard. People are suffering. The earth is suffering. It will get worse.

You know, since everyone loves the Nazi comparisons, there were people during the HEYDAY of the Third Reich who NEVER said, “We’re fucked.” They said, “We’re in a fight.” And you know what’s interesting? Nazi Germany went from the worst regime in the world to a liberal democracy within a lifetime. 

Look at Japan. Take the historical view. Stop pretending that the worst of what’s happening now is what is going to always happen. This is what is happening RIGHT NOW. That’s all you know. If you think it’s going to be this way forever, read a book.

Countries slide into fascism for long periods. It happens. Countries also have short-term extremist right-wing governments. Happens in Europe all the time. They get voted out. The threat remains. The threat of fascism will remain in America in a way it never has before. It’s a real movement. But we’re not fucked. Not even close. We can get off the ropes in the mid-terms and knock them out in 2020. But only if we stop saying that we’re fucked, and start seeing this as a fight.

I’m no Pollyanna. Things are so unutterably bad that I walk around in a constant state of nausea and horror. But you have to take the historical view, and you can’t lie down and say we’re doomed, or else they have beaten you.

Again, I don’t want to shame anyone who says, “We’re fucked” as an emotional reaction. I get it, I really do. But if you say that as a historical reality, then you SHOULD be ashamed. We are so far from being fucked. It's time for that warrior spirit, from everyone. 

Our best bet, actually our only realistic bet, is to mobilize the vote. There has always been a silver lining to this situation. I have always hesitated to state it, for fear of sounding like I am not taking the horror seriously. Fuck that; I do. But there has always been the possibility, there remains the possibility, that this is a time when our country faces up to its worst reflection, sees it truly, and breaks the fucking mirror. A time when the last bastion of white power and male supremacy and oligarchy attempts to enact fascism, but the antibodies of the American system and American multi-culturalism kick in to reject it. 

Where do you want to stand in that equation? As someone who rolled over because we’ve have had two awful years of shit that much of the world has already experienced many, many, many times over, so you decided that we’re finished and done for? Come on. Look at Europe, look at Africa, look at Asia. Back and forth with this shit, and much worse. 

I have your back. Get up. Here’s my hand. Let’s fight. 

It can’t become hip to give up. It can’t become hip to say we are fucked. Look at history. People have been so much more fucked than us, and won. If you truly believe we are finished, I’m sorry, but you were the first to fall. Stick a fork in you, turn you over, you’re done. I don’t want to see you do that, if only for the selfish reason that we need you.

Do all the protests, do all the direct action, make all the phone calls, then mobilize in October and November. That’s when we can get off the ropes and start punching again. Take the long view, my sisters and brothers. Don’t let them take you out of the fight. 

And if you need me for anything, I am here."""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
