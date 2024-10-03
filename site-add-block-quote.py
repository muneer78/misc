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
I will preface this by saying that this story is long, and I was not the mastermind to all the revenge that follows, but I did play a crucial role, and feel as though I need to explain my reasons for doing so.

I grew up in a single parent family, my mum, me, and my older sister, who, for this story's sake, I will call Lilith. Lilith is four years older than me, so the main reason I believe she was the way she was, was because she grew up an only child with both our parents spoiling her and giving her everything she wanted. Then I came along, and she wasn't the baby anymore. Then when I was two, my parents divorced, my dad moved away, and my mum was left alone with us.

My sister was, and still is, a grade A bitch. When I was growing up she used to bully me relentlessly. She would call me names, brake my stuff, blame my parent's divorce on me and even physically abuse me until I got old enough to hit back. At school, she used to get all her friends to bully me as well, and because a bunch of older kids were always cornering me, calling me fat and ugly, I never had any friends. No one wanted to be anywhere near me because of her, and she always made a point of letting me know just how much better then me she was. When I was younger, I believed she was better. She was prettier, wore better clothes, had a ton of friends and was into girly stuff like makeup and fashion while I was still in my teddy bear barbie stage. You could just tell me that this is all stupid kids stuff, but it only got worse as we got older.

By the time she was sixteen, I was just turning twelve, and the bullying had never ceased. Because of the type of person I was, I thought that if I did everything she said, she might actually like me, but this only encouraged her to take advantage of me. Things like cleaning her side of our room, getting her drinks, making her food, doing any housework mum asked her to do, and even giving her my pocket money, were completely normal. But despite doing everything she said, she was always nasty, and not just to me.

One of the worst memories I have of my sister is her screaming at my mum because she couldn't get the prom dress she wanted. I watched my mum try to explain that she didn't have the money to afford the dress she asked for and that she'd have to get a cheaper one. Lilith blew up on my mum, telling her they would have the money if dad was still here and it was all her fault that he left, and she shouldn't suffer because mum was too lazy to get a real job. This really struck a chord with me because even when I was younger I always noticed how tired my mum always was. She worked two jobs just to get us by, and for Lilith to act that way and say things like that really got to me. She made my mum cry that night, and I've never forgiven her for it.

Sometime later and my mum was dating this guy (we shall call him Matt). Matt was, and still is, great. He was really nice to all of us, bought us presents, made a point to get to know us, even took both me and Lilith on separate days out so we could both spend some alone time with him, which always made me feel special. I was thirteen when they got married, and we moved in with him. Matt made quite a lot of money, so both Lilith and I now had separate bedrooms and I could not have been happier. Enter Matt's son. Our mastermind. We shall refer to him as Megamind.

I had met Megamind a few times before my mum got married to his dad, but never really got to know him. He was older than me, but younger then Lilith, so when we moved into his house, I was terrified that Mega would be like Lilith. However, I was completely wrong. Mega was (and still is) the best brother. He never made me feel like I was unwanted. He let me play on his consoles, got me into reading, helped me with my homework, even encouraged me to make friends knowing how my sister's treatment of me affected my trust in people. Mega was the sibling I always wanted and never got to have, and Lilith just kind of faded into the background for a while. Then, some years later, Mega brought a friend home from university. His name shall be Nick. Nick and Mega were best friends. They did practically everything together, and had the truest bromance of any two men I've ever met. But there was evil lurking. Evil that wished to break the bromance forever. The first time Lilith saw Nick, I swear there were stars in her eyes, and she had to capture this innocent soul into her trap, by any means necessary. And poor Nick. Poor poor Nick.

Despite both me and Mega telling him repeatedly what kind of person she was, Lilith entranced this innocent boy with her looks and her charms and they soon started dating. Soon, whenever Nick would come over to the house to hang out with Mega, Lilith would show up and drag him away, making it all about her. She started arguments with Mega about spending to much time with HER boyfriend and that he needed to stop and leave them alone, to which Mega always laughed in her face and told her, not too kindly, to fuck off. Mega wasn't like me. He didn't take any of her shit and I deeply respected him for that. However, this evil demon was not used to being disrespected and so she hatched a wicked plan.

She started trying to separate Mega and Nick. If Nick came over to be with Mega she would always make him feel guilty about not spending enough time with her. She would start fights with Mega and then act like the poor victim over texts to Nick, Nick would then call Mega all upset and angry and Mega would try to explain that Lilith was just trying to manipulate him. All of this I saw as a spectator. Mega would tell me every time Lilith did something sneaky to try and brake his friendship with Nick, and I believed everything he said because I knew what kind of a person she was.

Then one day, Lilith and Mega had a massive fight. Our parents had gone on a couples weekend getaway and had left Lilith in charge since she was the oldest. I was about fifteen at this time, while Mega was nineteen and Lilith was twenty. Because she was the one in charge, she got given the money we were supposed to use for food. But of course, Lilith took the money for herself and bought a bunch of shit just for her, including, I remember, a pair of gold high heel shoes. They were pretty, but we couldn't eat them. Mega blew up on Lilith, and Lilith shouted back that she was older, better, and deserved it blah blah blah. Mega got our parents on the phone, told them what happened, and they ripped into Lilith, telling her to give her pocket money to Mega so he could look after us and buy us food for the weekend. Lilith shouted and cried but eventually gave in, never having successfully manipulated Matt in her life. She handed the money to Mega with a snarl, then spent the next few hours on the phone to Nick, wailing about how we were BOTH being mean to her while our parents were away and could she PLEASE stay at his house so she wouldn't be BULLIED anymore. Nick came running, and started screaming at Mega for, quote, "taking Lilith's money and getting her into trouble." Meanwhile, Lilith stood behind Nick with a smug look on her face while Mega was trying to explain. Nick then yells that Mega's been against their relationship from the beginning and he didn't know what Mega's problem was, but if he was forcing him to choose between him and Lilith, he chose his girlfriend.

Now I know a lot of you will call Nick stupid, but don't. I knew how manipulative Lilith could be. She was a master at making people feel sorry for her, and getting them on her side even when she was horrible to them, just like she did with me. That night I had to listen to Mega cry for the first time since I knew him, and I had enough.

I knocked on his door, asked him if he was alright, we ordered a pizza, and we started to plot. Mega was rather defeated by this point but I told him that if his friendship with Nick meant anything, he had to get him away from that demon spawn before he lost his friend for good. And so we plotted.

Lilith spent the entire weekend with Nick, and came back all happy and smug, rubbing it in Mega's face that Nick had chosen her, but via our plan, Nick said nothing back, acted defeated and let her talk. For the next few weeks, that's all she did. Whenever Nick came over to the house, she would spend time with him in her room, and when he'd leave, she'd prance around Mega, bragging about how much Nick loved her and asking Mega snidely if he missed his 'little friend'. Everytime she did this, her focus was entirely on Mega, she never once looked at me, and that was her biggest mistake.

Finally, the day of her twenty-first birthday had arrived. Nick and Mega hadn't spoken in weeks, and the few times Nick had gingerly tried to make things up with Mega, Lilith would walk in screaming about how he had already chosen her and that if he wanted to be friends with Mega again, then their relationship was over. Nick would always look miserable, but would side with her nonetheless. Mega had had enough. The fact that Lilith was making his best friend so unhappy purely for her own selfishness, snapped something in him, and he told me it was time to put our plan into action.

This was where my part of our plan finally took centre stage.

For her twenty-first birthday, she'd arranged to have her party at the house since it was huge, and more than enough space for all of her university friends. Our parents had agreed but only under the condition that there was no underage drinking and that both Mega and I were allowed to stay in the house. My sister reluctantly agreed, and thus the plan was in motion. On the morning of her birthday, I knocked on her bedroom door. She looked annoyed to see me and asked me snidely, "What do you want?"

I innocently told her I'd had the best idea. I told her I wanted to record her for her twenty-first birthday. I wanted to record her getting ready with her friends, talking about her plans after leaving university, record all her friends at the party, then set up the recording on a big projector Matt had in his office, so everyone could see it. This was before the time where smartphones were everywhere, so recording yourself was still something of a novelty, and I was using an old-fashioned camcorder I had gotten a few birthdays ago. Now, despite the fact that she did not like me, her wrath had been focused on Mega for so long that she most likely never saw me as a threat. And because of this both her and her friends seemed to love the idea.

I spent the entire morning with them. Recording them all getting ready, putting on their makeup and, of course, introducing themselves to the camera. My sister was lapping it up. She looked into that camera's eye like she was a supermodel movie star, preening and talking loudly about her successful future and how amazing her birthday party was going to be. That day I reverted back to my old role as a servant, fetched her and her friend's drinks and food, and made a grand show of complimenting all of them, and telling them how amazing they looked on camera, and that they could all be actresses some day. They were loving it.

So, the party starts, and my sister told me to stay out of the way. I told her innocently that it was no problem. That I'd just stay in my room all night, edit the recordings, and come down to set up the camcorder when she was ready, because I wanted this night to be perfect for her. Satisfied with my answer, she left my room.

And I did exactly what I said I'd do. I edited my recordings.

A few hours later, and one of her friends came to my room and told me she was ready. I set up the projector in the large living room, connected it to Matt's computer, and started playing the recordings for all her guests to see. The first part of the recordings were exactly what I promised. My sister and her friends introducing themselves and laughing in her bedroom as they had been hours earlier. I looked at my sister, who seemed so satisfied that all the attention was on her, then I looked at Mega, who was hiding in the corner of the room, and gave him a subtle thumbs up.

Then the video started to change. It started to play clips of Lilith shouting at Mega, calling him names and taunting him about Nick. It started showing Lilith snidely telling Mega that Nick belonged to her and that she was going to do her best to make Nick hate Mega, so they would never be friends again. It even showed clips of Lilith bragging about all the lies she'd told Nick and how he was 'so gullible'. Every single argument I had recorded without her knowledge I'd edited into this video.

Everyone in the party was watching silently as Lilith's true self was exposed in clip after clip, while Lilith stood there frozen, completely unable to comprehend what was going on. When she finally snapped out of it, she turned on me, and started screaming, yelling at me and asking me "How could you do this?"

I never said a word, I just smiled.

When the recording stopped, Mega turned the lights on and everyone was staring at Lilith. Clearly having no defence, she let out a loud cry and stormed up to her room, slamming the door so hard everyone heard it.

The next day Mega told me Nick had apologised for everything, and that he was stupid to so blindly believe everything she said. He even told me that Nick had thanked me specifically for helping him see what a monster my sister truly was. When my parents came home, both Mega and I were grounded for ruining Lilith's birthday and for using Matt's stuff without permission. But neither of us cared. Mega got his best friend back, and a few months later, Lilith moved out, since, after seeing the recordings of her behaviour, my parents were disgusted by her, and they had absolutely no problems with showing it. Since she no longer had any leverage over anyone in the house, she packed her bags and moved to stay in one of her college dorms. I've never had any problems with my sister since, and to this day Mega and I are as close as two siblings can be, and always laugh about the time we defeated the demon and saved us all from its clutches.

TLDR: My sister tries to separate my brother from his best friend, so we humiliate her on her birthday.

Update: Thank you so much for the support, and the gold! For everyone asking what happened next, well...

Mega and Nick are still best friends. Mega was the best man at Nick's wedding, and before you ask, yes, he learned his lesson about dating witches, his wife is sweet as a cherry drop.

Mega's happily living his life as a single man for now, and is currently working as a carpenter/restorator.

I'm in a very healthy, very happy relationship with my man of four years. We're not married but I'm hoping soon...

And as for Lilith, well, I don't see much of her these days. Last I heard from mum, she was living alone somewhere near the seaside, is working in one of those arcade places and still gives as many fucks about us as we do about her. She only ever comes home to ask mum and Matt for money, and hasn't talked to either me or Mega in a LONG while. As much as I'd like to say she learned her lesson, I don't see her personality changing any time soon. Nonetheless, Mega and I are still really close, and Nick and I always joke about who's going to be the best man at his wedding.

Update 2: For everyone calling out my parents for not doing anything to stop Lilith's behaviour, I'd like to first point out that we were all pretty private kids. I suffered from social anxiety and Haphephobia well into my early twenties, so when I was a kid watching all of this shit go down, I just followed Mega's lead since he was my hero. As for Mega, well, he actually lived with his mum for the first half of his life, and only visited his dad a few times a year since they lived so far apart, but his mum passed, so he had to up route his whole life to move in with Matt, then a while later he inherited a mother, a nervous younger sister and a bitchy demon spawn. That's probably why he never really spoke to his dad about what was happening all those times, because Mega and Lilith have gotten into many petty fights over the years, I could tell many stories, but they kept all the warfare silent, neither wanted to involve our parents.

And as for my mum and 'Matt' well, I don't really know what Matt was feeling beyond loving my mum, but I know that my mum put a LOT of herself into her relationship with Matt. Not meaning that she loved us any less, but after my dad left, we had to downsize our whole life, and she had to get two jobs to look after us all. So, when she met this amazing guy who literally swept her right off her feet, let her quit one of her jobs so she wasn't so exhausted, bought her kids gifts and genuinely cared about ALL OF US, I think she let herself go blind to some of the conflict in the house. It doesn't make her a bad person, I love her dearly, but Matt kinda became my mums top priority, especially since, by the time we all moved in with him, we were older and could fend for ourselves. So that's all basically why neither of them ever stopped what was happening. They either didn't really notice, or thought it was all petty kids stuff us young adults could sort amongst themselves. There are times I think she should have done better, but she was literally miserable before she met Matt, even though she tried hard to hide it, and now she's happy, I just can't bring myself to reprimand her for not seeing all the stuff that happened YEARS ago.
"""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
