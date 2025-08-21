# Example text to be blockquoted
text_to_blockquote = """A few things spring to mind…

Trump lacks certain qualities which the British traditionally esteem.

For instance, he has no class, no charm, no coolness, no credibility, no compassion, no wit, no warmth, no wisdom, no subtlety, no sensitivity, no self-awareness, no humility, no honour and no grace – all qualities, funnily enough, with which his predecessor Mr. Obama was generously blessed.

So for us, the stark contrast does rather throw Trump’s limitations into embarrassingly sharp relief.

Plus, we like a laugh. And while Trump may be laughable, he has never once said anything wry, witty or even faintly amusing – not once, ever.

I don’t say that rhetorically, I mean it quite literally: not once, not ever. And that fact is particularly disturbing to the British sensibility – for us, to lack humour is almost inhuman.

But with Trump, it’s a fact. He doesn’t even seem to understand what a joke is – his idea of a joke is a crass comment, an illiterate insult, a casual act of cruelty.

Trump is a troll.

And like all trolls, he is never funny and he never laughs; he only crows or jeers.

And scarily, he doesn’t just talk in crude, witless insults – he actually thinks in them. His mind is a simple bot-like algorithm of petty prejudices and knee-jerk nastiness.

There is never any under-layer of irony, complexity, nuance or depth. It’s all surface.

Some Americans might see this as refreshingly upfront.

Well, we don’t. We see it as having no inner world, no soul.

And in Britain we traditionally side with David, not Goliath. All our heroes are plucky underdogs: Robin Hood, Dick Whittington, Oliver Twist.

Trump is neither plucky, nor an underdog. He is the exact opposite of that.

He’s not even a spoiled rich-boy, or a greedy fat-cat.

He’s more a fat white slug. A Jabba the Hutt of privilege.

And worse, he is that most unforgivable of all things to the British: a bully.

That is, except when he is among bullies; then he suddenly transforms into a snivelling sidekick instead.

There are unspoken rules to this stuff – the Queensberry rules of basic decency – and he breaks them all. He punches downwards – which a gentleman should, would, could never do – and every blow he aims is below the belt. He particularly likes to kick the vulnerable or voiceless – and he kicks them when they are down.

So the fact that a significant minority – perhaps a third – of Americans look at what he does, listen to what he says, and then think

‘Yeah, he seems like my kind of guy’

is a matter of some confusion and no little distress to British people, given that:

Americans are supposed to be nicer than us, and mostly are.

You don’t need a particularly keen eye for detail to spot a few flaws in the man.

This last point is what especially confuses and dismays British people, and many other people too; his faults seem pretty bloody hard to miss.

After all, it’s impossible to read a single tweet, or hear him speak a sentence or two, without staring deep into the abyss. He turns being artless into an art form;

He is a Picasso of pettiness; a Shakespeare of shit.

His faults are fractal: even his flaws have flaws, and so on ad infinitum.

God knows there have always been stupid people in the world, and plenty of nasty people too. But rarely has stupidity been so nasty, or nastiness so stupid.

He makes Nixon look trustworthy and George W look smart.

In fact, if Frankenstein decided to make a monster assembled entirely from human flaws – he would make a Trump.

And a remorseful Doctor Frankenstein would clutch out big clumpfuls of hair and scream in anguish:

‘My God… what… have… I… created?’

If being a twat was a TV show, Trump would be the boxed set."""

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