# Example text to be blockquoted
text_to_blockquote = """""Texas and Florida have a lot of similarities," Baker told reporters.

"Some people don’t like fearing for their lives on a simple 7-Eleven run for a single 32-ounce can of Busch Light. Personally, that’s part of the magic.

In Florida, a man with an unwashed ass driving a dent-riddled Ram 1500, 37 dings from 37 separate collisions, will ride your ass on I-4 because you’re not riding the guy’s ass in front of you hard enough.

The back of his truck is a fever dream of yellow snake decals, skulls, and political rants, all directed at whoever’s unlucky enough to be behind him. It’s a perfect ecosystem of rage and insecurity, one that keeps the fragile ecosystem of I-4 chaos alive.

Every car in that convoy to hell they call I-4 is piloted by someone terrified, armed, and one brake tap away from turning the worst highway in America into a smoking parking lot.

That Ram driver btw? Online, he portrays himself as a warrior. Loyal but dangerous. In reality, he’s neither of those things. He’s just scared. Scared of everything. And the only way he feels safe is if everyone around him is scared too.

From the outside, it sounds miserable. But live here long enough and it starts to make sense. Every hurricane season, people around Tampa wait to see if the next storm will wipe out everything they love... And the dark part is... Deep down, a part of them almost hopes it does.

I get it. It’s not supposed to sound appealing. But I love the Mad Max movies, and every time I grab a Pub Sub here, I feel like I’m living in that universe. It’s beautiful chaos. It’s home."
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