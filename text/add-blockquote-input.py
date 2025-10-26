# Example text to be blockquoted
text_to_blockquote = """I (24f) live with my cousin (30m). I have three cats (one adult cat and two 12 week kittens), and whenever I am home he will be “mean” to them in a very joking and lighthearted way. He’ll call them names (fatss, dumbss, etc.) but it’s in that “bullying as a love language” type way and I have never been afraid of him actually mistreating my cats, especially because they clearly adore him. He plays and rough houses with them, he pets them, but he never gets all lovey dovey the way I do with them…. Or so I thought.

I live in a two story townhouse with my bedroom being on the second floor and I always keep my door open so that the cats can go in and out. Yesterday morning I had woken up but not gotten out of bed yet and my two kittens were playing on the landing just outside my bedroom door.

I hear my cousin start to walk up the stairs and I stayed as quiet as possible. I knew he thought I wasn’t home because when I am home he always calls up to me to ask if he can come up (I have given him permission to go in my room when I’m not home to play with my cats).

My door was cracked open about a foot and I see his arm reach, he says “Scoop!” And grabs a kitten. Then I hear about a minute straight of kissy sounds and baby talk.

I’m just quietly watching from my bed, trying not to let out a giggle, when he suddenly stops, slow turns, and makes stunned eye contact with me through the crack in my door. When he realized I saw/heard the whole thing he got embarrassed and said “oh… I uh.. I saw them running around up here and thought I’d come play with them.”

I laughed and said it was totally fine, but he retreated back downstairs to put his tough guy persona back on.

The photo above is one he just sent me having a cuddle session with baby George

Tl;dr: my male roommate pretends to be indifferent about my cats, but secretly baby talks and loves on them when I’m not around

Text messages between OOP and the roommate

Roommate: He’s been here for like 20 minutes

Pic of the cat on the roommate

OOP: :face_holding_back_tears:

OOP: He’s so sweet

End of transcript

Editor’s note: description of the picture – A heartwarming moment is captured of a light-colored feline curling up on the roommate’s lap. The roommate is resting on a couch with his legs stretched out on a couch with a blanket nearly.

 

Update: August 23, 2025 (2.5 months later)

A while back I made a post about how I caught my roommate baby talking my cats, and I have a new adorable development.

A couple months ago I went on a family vacation so my roommate took care of my cats while I was gone. During that week, he accidentally started a new routine with them.

Each time he’d fill their food bowls, he’d stand there and give them pets and scratches while they ate. After a couple days, they decided that that is now a requirement. Only with him though, they don’t make me do this.

Now, every day when he gets home they run to the door to excitedly greet him and then run to their food bowls. They’ll sit there and yell at him until he goes over to give them pets while they eat.

The funniest part of it is that they free feed. I just keep their bowls full so that they can eat whenever they are hungry (I know some people frown upon that but my work schedule is too unpredictable to keep them on a consistent feeding schedule and none of them are overweight, so it works for us). Even though they have constant access to food, they’ll wait for him to get home from work to have dinner so that he can give them scritches. So sweet
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