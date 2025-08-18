# Example text to be blockquoted
text_to_blockquote = """The role of the president in our new American imperial system is to consolidate power by putting his people in charge of the game. You can rig an election by changing the district boundaries so that voters have no hope of getting representatives from the opposition party, and by suppressing or changing the official statistics we use to tell stories about the economy.

And to be clear, this is not a question of policy outcomes or political correctness. Democracy is on the line.

In the view of the authoritarian leader, democracy is something to be undermined, a referee to be bribed, not a method by which legitimate opponents can derive power from the people. To Trump, the only legitimate outcome is the one where he comes out on top. Anything that undermines that end is now a threat. That means that he will say that elections are rigged when he’s losing, and that he’ll fire the referees when he’s caught scoring an own-goal. Just like the only legitimate election is one where Trump wins, the only legitimate data now is data that shows him succeeding.

The unified theory of Trumpism is that loyalty to Trump is not simply a product of party competition of political game theory; loyalty to Trump is the ideology. Trump himself is now effectively the entirety of the Republican Party’s platform. If this were not politics, and if American journalists did not have a false pressure toward neutrality, we would call what has happened to the GOP under Trump a personality cult, not a political program. Any policy, principle, or person that conflicts with Trump’s will is disposable. From data to districts, from bureaucrats to ballots, all must serve the Leader or be cast aside. That’s not a party, that’s a cult."""

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