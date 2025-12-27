# Example text to be blockquoted
text_to_blockquote = """Rather than exert so much energy trying to thrust Trump out of the presidency, liberals would be well served to spend their time thrusting the presidency upon Donald Trump. Instead of searching for illusory quick fixes for the existence of the Trump administration, start demanding the Trump administration fix everything quickly.

If there’s one thing we’ve learned from the sample size of one Trump presidency and his four years out of power, it’s that Trump is a bog-standard rich white guy whom the justice system is largely incapable of bringing to heel. He has powerful friends (oligarchs, Supreme Court justices), deep pockets, and a well-tempered ability to joust in the media. By now we’ve watched ol’ Donny “wriggle out of this one” on multiple occasions; he seems to thrive if you put him at the center of something he can deem to be a witch hunt—even when those hunters bag their quarry, as prosecutors did in his hush-money case.

But Trump has historically faltered when he’s been forced to contend with the actual pressure of the presidency and its myriad responsibilities (see also: the Covid-19 pandemic) because his ideas are bad and he doesn’t have a deep and abiding interest in public service to really make a sustained effort to confront, let alone solve, the biggest problems we face.

President Barack Obama found the presidency to be an exhaustingly taxing job, so much so that he famously went to somewhat mind-blowing lengths to limit the nonpresidential decisions he had to make in order to stay keen enough to handle the toughest of the choices on his plate. Trump, by contrast, mostly showed up late to work and watched cable news all day. Had the coronavirus not emerged as a global threat, he might have made it through his first term having not felt the pressure of the job at all. In his second term, it should be the task of liberals to force Trump to swallow a daily spoonful of the very real job stress that Obama struggled so mightily to endure.

To get there, liberals need to get into the business of identifying the problems that real Americans face (which honestly, is something they could stand to relearn how to do) and more forcefully blame Trump for those problems’ continued existence. They need to raise a hue and cry over everything under the sun that’s broken, dysfunctional, or trending in the wrong direction; pile line items on Trump’s to-do list, wake him up early and keep him up late. Every day, get in front of cable news cameras and reporters’ notepads with a new problem for Trump to solve and fresh complaints about the work not done.
"""

def add_blockquote_to_text(text):
    """
    Adds a Markdown blockquote character ('> ') to the beginning of each line
    in the given text and prints the result.
    """
    lines = text.splitlines()
    modified_lines = [f"> {line}" for line in lines]
    print('\n'.join(modified_lines))

if __name__ == "__main__":
    add_blockquote_to_text(text_to_blockquote)