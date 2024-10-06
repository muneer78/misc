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
Dear Men of Craigslist,

Look, I know you men have it difficult. Women are just about impossible to understand, much less please. In a post-feminist society, you never know exactly what you should be doing. Women are bloody picky, I know we are. It can be scary, too, when women freak out about what appear to be benign issues. And men who do their best to be respectful, female-positive humans, I salute you, I do.

But please, please just fuck me already. Honestly, I appreciate your thoughtfulness. I like that you want to take things slow. I can totally get behind the idea of emotional connection, but dearjesusinheaven, FUCK ME. We've done dinner and drinks. We've gone dancing. We've cuddled and watched a movie. I'm wearing a low cut shirt and you've been staring at my breasts all night. Goodgodalmighty, get to it and fuck me.

When we get hot and heavy, please take charge. Please, please fuck me. Trust me, I'm not going to just lie still - I'll get involved. But don't make me force your hand into my panties. That makes me feel like a rapist. We've been kissing for a half hour and your hand keeps grazing my ass. That's nice, but it's time to move forward. Get on top of me. Don't make me get on top right out of the gate and start bobbing up and down on your cock like I'm practicing some crazy new aerobic yoga because YOU won't go down on me. Roll on top and start dry humping like a good boy should. Don't gently suck my nipples and then pull back when I moan with pleasure. You being coy is totally not what I want. It's not what WE want.

OK, I know it's scary. There are lots of women out there who make fucking really difficult. So, I have compiled some handy tips. Don't think of this as complaining, or as schadenfreude for the Andrea Dworkins of the world. Just some simple tips, for timid men who have forgotten what it means to fuck like men:

1. Taking charge is not bad. Oh, there will be some women who feel that you are pushy. If you are making out with a woman, and she starts to push back, ask nicely if things are moving too fast. If she says yes, say something like "I'm sorry - you just look so fucking delicious. I'll go slower." Otherwise, skillfully move forward. If you start kissing a woman, and she responds well, and before long, you're both on the floor with her skirt pushed up, and you on top of her, it's not the time to roll onto your back and start awkwardly stroking the top of her head. Seriously, grow a goddamn pair. YOU'RE the man. Act like one.

2. Ohmyfuckinggod, please learn to respect the clit. It's different for every woman, so ask what she likes. Do not, I repeat, do not just wiggle your fingers around her pussy like you're trying to tickle her. Do not drum your fingertips against her vulva like you are impatiently waiting at the Sears Tire Center for your receipt. Do not push the clit like it is a doorbell at some house that you need to get inside of. Start by using all four fingers with firm yet gentle pressure against the outside of her pussy. Do not charge in with a single finger and start jabbing at things. And if you really don't know what to do, ask her. Just ask. "How do you like it?". It's a simple question, and most women will answer straight out. If she's being all coy, ask "Do you like pressure? Is it sensitive?" The clitoris is a varied item, indeed. Treat each one as though you have never encountered one before. Forget everything that your last partner liked.

3. Most women like to be fucked, and fucked well. Yes, there are women out there who want to "make love" every time - sweet, gentle, rocking love with lots of eye contact and loving kisses. Those women are not the majority. The majority like to be pounded. The majority like to have their hair pulled. The majority like a good, solid jackhammering. When a woman is bucking wildly against you, it's not because she wants you to pull back and slowly swirl your cock around her vagina like you're mixing a cake batter up there. It's because she wants you to hold down her arms, or grab her hips, or push her legs above her head, and fuck her harder. Don't be too afraid of what this means as far as gender equality goes - I am a raging feminist bitch, but I still want to be penetrated like you are planning on fucking my throat from the inside out.

4. A little roughness is nice. Do not pretend that you had no idea that some women like their hair pulled. Do not act shocked if she wants you to spank her ("Really? Spanking? Won't it hurt?" - yes, it does. That's the fucking point). We know you've read Stuff and Maxim, and that's all those laddie mags talk about in their "How to Please Her" sections. Start with light, full handed smacks to the area of her ass that she sits on. Judge her response and continue on from there. You don't have to bend her over one knee and tell her she's a naughty girl and that Daddy's going to punish her; save that for the fifth date. Women are less delicate than you think, so don't worry about breaking her hip.

5. It's OK for you to make noise. Otherwise, we feel like we are fucking a ninja. Unless you actually are a ninja, and have sneaked into our rooms with vibrating nanuchaku and zippered black pajamas, please, please make some noise. If you're banging a woman, and she's crying out and saying your name and moaning, and you can't even manage a grunt, she's going to feel like an idiot. You don't have to make the sounds she is making, but do SOMETHING. You know how when you are watching porn, and the girl does something great to the guy and the guy kind of goes "Ah!", half grunt, half yell? That's HOT. Do that. Whisper our name (assuming you know it) gruffly. Groan against her neck when you're in missionary position. You don't have to grunt like a mountain gorilla, but if you are totally mute, she's going to get worried.

6. Most women like dirty talk, in addition to the grunting. If you'd like to get some dirty talk going, ask her if she likes the way you fuck her. If she responds well, continue with something like, "I love fucking you. God, you look so fucking hot." Is she still moaning in response? "Your tits are so beautiful." Does that work? If she doesn't respond well to the term "tits", you might have to stop there. If she keep moaning or responding, pass Go and collect $200. Try the following:

"Oh, god. Your pussy is SO tight."
"You're so wet - are you wet because you like the feel of my cock ramming you?"
"I think I'm going to come inside you. I'm going to fill up your little cunt." It doesn't matter that you're wearing a condom; we LOVE hearing this.

If all of those work, you can then progress to things like "sexy little bitch" and "dirty whore". Tread carefully, but please, tread. Do not tiptoe. Do not sit down. Charge.

6. You're not obligated to eat a woman out. In return, she's not obligated to choke on your dick. Don't skip one and expect the other. If you do eat a woman out, the only comment you should make about her pussy is how nice it is. The length of her labia minora, the color of her interior, her waxing job or full bush - you are not John Madden. No time for color commentary.

7. Do not bitch about condoms. Oh, we hate them. Trust us. They hurt us more than they hurt you. But we don't want to be preggers, and you don't want to catch anything, right? Don't whine about condom sex. Do not explain that you can't come with one on. LEARN to come with one on, or if not, help us figure out what to do with you once we're satisfied and it's time for you to let loose your load.

8. We really like it when you come. It's called a money shot for a reason. Watching semen shoot out of you is one of the most gratifying things EVER. However, do not assume that she wants you to jack it off onto her face. She might, but don't assume. Seeing and/or feeling you come is rewarding for us, so there's no need to deprive us of it, but please do consult us before unleashing. "I think I'm going to come - how do you like it?" is a fair question that shouldn't rob you of your testicles.

In recent memory, I've been fucked by a very aggressive, manly guy, and I've been... well, fucked is the wrong term here. I've been penetrated by a total and utter wuss. Who am I going to run back to when I'm ready for my fill? Manly McHardon, that's who. ----------------------------------------------------

*New point of clarification - some people have brought up some really great issues in response to this post, so let me say this: I don't mean to imply that all women like to be treated like whores. I do mean to say that most women I know have told me that they like sex rougher than most men give it to them. Rough does NOT equal chains and bondage. And this applies to the bedroom only, and does not mean that she wants you to choose her dinner for her, or treat her like less of a person. **Some women have said that they don't like it rough and what the hell am I thinking? Well, girls, you're in the minority. HOWEVER, all women need to remember that, in addition to be straight forward about your sexual desires, you need to be straight forward about your sexual limits. Don't be afraid to ask for more, but when something feels wrong, say so. Don't ever do something you don't want to do in silence and then blame the guy. Silence is dangerous.
"""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
