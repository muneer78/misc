import re

def convert_html_to_markdown(text):
    # Step 1: Replace <p> and </p> tags with line breaks
    text = re.sub(r'</?p>', '\n', text)

    # Step 2: Replace <img> tags with markdown image syntax
    text = re.sub(r'<img src="([^"]+)" alt="([^"]+)"[^>]*>', r'![\2](https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/\2)', text)

    # Step 3: Replace <hr> tags with horizontal rule
    text = re.sub(r'<hr>', '\n___\n', text)

    # Step 4: Remove empty <p></p> tags and excess newlines
    text = re.sub(r'\n{2,}', '\n\n', text)  # Reduces multiple newlines to a maximum of two
    text = re.sub(r'<p></p>', '', text)

    # Step 5: Replace blockquote <blockquote><p>...</p></blockquote> with markdown blockquote
    text = re.sub(r'<blockquote><p>(.*?)<\/p><\/blockquote>', r'> \1', text, flags=re.DOTALL)

    # Remove any remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    return text.strip()

html_text = '''
<p>I got a call on a Thursday afternoon from [Suzie]. It was a curious call because the address on the intake form was a Canadian address. Prepaid Legal only sold plans to people in the US. Suzie had met [Gavin], a Canadian, online. After a whirlwind romance, Suzie and Gavin decided that they live together in Ottawa, where Gavin was living. They packed up all of her things into a U-Haul and then hitched her car to the U-Haul on a trailer.</p>

<p>The couple set out for the border crossing near Buffalo, NY. As Suzie and Gavin reached the border, the Canadian immigration officials asked if them if Suzie was emigrating or coming to Canada for vacation. Suzie replied that she was coming for vacation. Since most vacationers don’t bring 4 rooms worth of furniture and a car on a trailer for a vacation, Suzie was turned away at the border. At this point, Gavin got out of the truck and hitched a ride to Ottawa with another driver.</p>

Suzie was now stuck in Buffalo. So she called her friendly home state PPA firm. Since I was the only one who knew anything about immigration, I got to take the call. This led to the following exchange:</p>

**Suzie**: I only have enough money to stay in this motel until Tuesday! I got the forms right here. You think this will all be sorted by then?<br />
**Me**: I highly doubt that you will be able to apply for and secure a residence permit in Canada in three and a half days.<br />
**Suzie**: What?? I didn’t even think you needed a passport to go up to Canada. [Note: this conversation took place in 2009.]<br />
**Me**: You can go up to Canada for a visit without requiring a passport or visa, but you cannot emigrate there without a visa.<br />
**Suzie**: Well what do I do then?<br />
**Me**: I would suggest asking your fiancee to get you an attorney in Canada to assist you with the process.<br />
**Suzie**: You mean I don’t get this taken care of for free? Why am I paying you $19.95 per month?<br />
**Me**: I can advise you on US immigration law, but you need someone who is licensed in Canada. You will need to go through Canada’s procedure for emigrating.<br />
**Suzie**: I don’t have any money to stay in this motel past Tuesday! I thought this would be done by then!<br />
**Me** I am sorry to disappoint you.<br />
**Suzie**: Where am I supposed to stay??<br />
**Me**: You could always come back to [my state].<br />
**Suzie**: I can’t! You have no idea how tough it was to get up here with all my stuff!!<br />
**Me** Well, then I suggest you get a residence and a job in Buffalo. This is not going to be a quick process.<br />
**Suzie**: This is so unfair! Why do I pay you guys $19.95 a month??</p>
'''

markdown_text = convert_html_to_markdown(html_text)
print(markdown_text)
