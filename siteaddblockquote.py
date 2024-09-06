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
This was a really cool story that Mike Rowe posted to Facebook:

> "Last week in Baltimore, Uber charged me $85 for a trip that usually costs $20. I looked into the way their "surge pricing" model actually works, and didn’t like what I learned. So today, after checking out of my hotel in Oklahoma, I called Lyft instead and was picked up by a guy named Mike. He was driving a red F-150. It was clearly a work truck, full of tools and lumber. I sat up front."

> “How far to the airport,” I asked.

> “Fifteen minutes,” he said. “You in a hurry?”

> “Not really,” I said. “Are you?”

> “Never.”

> As we merged onto the highway and settled into the slow lane, I asked Mike if he was a carpenter in real life.

> “Among other things,” he said.

> “Jack of all trades?”

> “Well, I don’t know about that,” he said. Back in the seventies, I was a plumber’s helper. Then I worked for a spell in the heating and air condition game.”

> “How was that?,” I asked.

> “Hot and cold,” he said.

> I honestly couldn’t tell if he was making a joke or not. His voice had a classic midwestern drawl, and there was no expression on his face as he stared out the windshield.

> “After that, I started carpentry. Trim, then framing. Then I moved on to building custom cabinets in rich people’s houses. Figured out how to build spiral staircases and furniture. Did pretty good.”

> “You retired now?

> “No. I build campers these days.”

> “What kind of campers?” I asked.

> “I build them small ones you can tow pretty much anywhere. They call ‘em teardrop trailers. Got really popular during the lockdowns. I build ‘em by hand, one at a time.”

> “Yeah? How’s the quality,” I asked.

> “Pretty good,” he said.

> “Got a website,” I asked.

> “Sure,” he said. “Gotta have a website these days.”

> “What’s your website called,” I asked.

> “Mike’s Pretty Good Campers.”

> I still couldn’t tell if he was messing with me.

> “Your company is called 'Mike’s Pretty Good Campers?'”

> “I like to manage expectations,” said Mike.

> "Under promise and over deliver?"

> "That's the idea," said Mike.

> "Is that what you were doing before you picked me up just now? Building a pretty good camper?”

> “Yup. But I was starting to get frustrated. And I don’t like to work when I’m frustrated. So, every now and then I gotta step away.”

> “And drive a stranger to the airport?” I said.

> “Never too frustrated to drive,” said Mike. “Driving relaxes me. Besides, we ain’t strangers no more, are we?”

> “No,” I said. “I suppose we’re not.”

> As we turned on Airport Road, I said, “So what’s the plan? Drop me off and wait for another call? Or head back to the shop and finish building that pretty good camper?”

> “Ain’t decided yet. Guess I'll see how I feel in a few minutes.”

> “Good plan,” I said. “By the way, if I like your website, do you care if I share it on Facebook?”

> “Why would you want to do that?” he asked.

> “I’ve got a few people who follow me on social media,” I said. "I'm not sure why they do, but they do. Maybe some of them are in the market for a pretty good camper, custom made by a quasi-retired carpenter who drives for Lyft when he’s feeling frustrated?”

> “Can’t hurt,” said Mike. “Once people see these things, they fall in love with ‘em. They got whole conventions all over the country for teardrop trailer owners. Thousands show up. You wouldn’t believe how people decorate ‘em and such.”

> "I don't know about that, Mike. I'll believe pretty much anything these days."

> As we pulled up to the airport, Mike asked me what carrier I was on.

> “American,” I said. “Right here is fine.”

> “Pre-check?” he asked.

> “Yes,” I said.

> “Well then, you don’t want to get out at American. Let me take you all the way to the end, otherwise you got a walk across the whole dang the terminal.”

> We pulled up to the curb at the very end of Will Rogers Airport. I hopped out, as Mike dragged my bags out of the bed of his work truck.

> “You look familiar,” he said. “Have I driven you before?”

> “I don’t think so,” I said. “I would have remembered. Thanks for the lift.”

> “No problem,” he said. “Was the ride okay?”

> “It was a pretty good lift,” I said.

> Somewhere behind his mustache, Mike might have smiled, as I walked into the only airport in America named for a cowboy who never met a man he didn’t like. There, I boarded my plane and checked to see if there really was website called “Mike’s Pretty Good Campers.”

> Son of a gun...

> Credit -  Mike Rowe
"""

# Apply the function to the input text
output_text = add_gt_to_blank_lines(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
