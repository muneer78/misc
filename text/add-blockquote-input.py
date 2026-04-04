# Example text to be blockquoted
text_to_blockquote = """Dad considered leaving the department entirely, but this posting proved to be a brief interlude before another high-profile assignment—the Tactical Patrol Force. The T.P.F. was a spit-and-polish unit of the sturdiest young officers, sent in to quell riots and make the big, sweeping organized-crime arrests that put the mayor and commissioner on the front pages.

He was leading this unit in arrests, and his career was off to the races again, when his path took another turn after another principled stand. He asked for the night off on the evening his first child was born, and when this reasonable request, well within his rights, was denied, he took the night off anyway. Saying no to the big time twice is twice too many times, and the next day, he was shipped out to Brooklyn to report for precinct duty.

But being exiled to the outer boroughs, doing anonymous, “flatfoot” work over the next two decades—first as a patrolman, then as a detective—turned out to be the work he loved. It was what he had signed up for: protecting and serving people trying to make something of their lives and their neighborhoods.

He never told us that he led the borough in arrests for several years running. He never told us about the decorations he received. But he told us of the family he made among his fellow patrolmen and detectives, and the good people they watched over.

There was a great irony along the way. His former colleagues on the vice squad were disgraced in the aftermath of the Stonewall riots in 1969, as many of them were discovered to be shaking down gay bars for bribes. The Tactical Patrol Force, once the department’s shining elite, was left to operate with impunity for too long and got their comeuppance when the Knapp Commission in the early 1970s revealed the unit to be rife with corruption. While my father’s career ended in applause at a community banquet, many of his former colleagues saw theirs end in humiliation and ignominy."""

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