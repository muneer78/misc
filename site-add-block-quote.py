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
To clarify, this is India so when I say truck, I don't mean SUV, IT IS A LITERAL LORRY FILLED WITH RICE

Update: BIL is now negotiating with lorry driver. My requests to keep phone on speaker so I can here have been coldly rebuffed. I can however confirm that bribe has been offered and rejected. I cannot say whether this was a question of principle or price

Update 2: BIL wants everyone reading this to know that I'm  dick for livetweeting it and this is not helping

as a horror writer, I can now confirm to ou with evidence that anything can be horror, I just watched a man's face curl up in abject terror at the words "Why Is It Still Outside My House?"

Update to Drama: BIL had come in to explain that driver insists they'll have to take the rice(and pay) but midway through thouht better of it and is now negotiating with driver again. An excellent demonstration of the flight instinct in mammals when confronted with mortal peril

Side update: They also apparently have to unload the rice themselves.

Update: Calls are now being made to owner of warehouse

Update: Warehouse Owner is not taking calls. Spot negotiations have resumed.

Also all of you enjoying this need to join me in thanking Mom for going above and beyond the call of duty and carrying phone between locations & also relaying key info while somehow also social distancing so we can continue bringing you our live reporting on this unfolding crisis

Update: BIL is making headway. Lorry driver and helper have accepted cigarettes from him. Negotiations have resumed while all 3 smoke.

Update: Lorry driver just laughed at something BIL said. BIL also laughing. Cigarettes may have been a masterstroke by BIL. We are moving our reporting back indoors to inform Sis.

Key Update: Cigarettes were in fact a huge strategic blunder because BIL apparently assured sis that he's definitely finally quit smoking on Sunday and in no way shape or form was supposed to have packs of cigs just there in pocket ready to be used as negotiating aid.

Update: Bereft of victims for the moment, sister is now asking me if I knew about this. There may be a slight lull in updates while I swear innocence and try to avoid becoming collateral damage in this tale of Indian Carnage

Update: I have convinced sister that I am not party to this. However Mom and I have fled back outside because dad just walked in and asked sis "what is this truck outside why did you call it?"

BIL Update: Warehouse Owner still not taking calls but they have reached some chappu of his who told them to call someone called Manu, he'll take care of it. Thats all we know about him. He's Manu, this his number and he'll take care of it.  He is the Mr Wolf of warehouse cockups

Update: Manu is not answering the phone.

Update: Dad has also come outside and joined outside reporting crew. Mom asked him why are you here and his response was why are YOU here?

We are all here

Update: Manu just called.

Manu is now speaking to lorry driver. Driver is getting animated. He is the real victim(I kinda agree)

Manu is now speaking to BIL.

BIL is getting animated

Manu has asked to speak to lorry driver again

Manu clearly believes in getting all sides in a conflict before coming to a decision because he is now speaking to lorry driver's assistant. A wise judge. Maybe he'll want to speak to me too. One can but hope.

Manu is now speaking to BIL again. So far he has shown no interest in speaking to us. This is humbling.

Mom is scolding dad for demanding to speak to Manu. Dad has been banished back inside as punishment.

Meanwhile Manu and BIL do not appear close to a resolution.

Dad attemped to break curfew and come back out. He has now claimed he's done with the whole thing and doesnt care and also where the hell is dinner and he is going to room to watch news because state of the world matters more than a ruddy truck. 
Valid points, but I am skeptical.

BREAKING NEWS: Manu Is Coming

First however, Manu obv has to talk to driver again. Manu seems to be a talker, he has lots to say to everyone.

Still nothing to say to me though. Hey Manu, nobody likes a snob, you know. I'm a person too.

Phone has been hung up. We are now waiting for Manu.

holy shit a lot of y'all care about my BIL and his misadventures with rice trucks. We're still waiting for Manu so consider this an ad break. Get popcorn, visit the loo, order some rice.

Update: Manu called again. He is lost and needs directions.

Mom is making everyone eat food while we wait. Ironically there is no rice on menu.

Update: Mom just called back. I think Manu may have arrived.

Ok we're outside(sorry bout delay, but we're dependent on mom who DGAF about anyone during dinner, even Manu)

Since I know I cared about this and was wondering, Manu kinda looks disappointingly average. He's just  normal, random desi uncle in shirt pant. Sad!

BIL is now making what appears to be a passionate case. Manu certainly appears sympathetic, he is nodding.

Manu is now nodding at what driver says. Manu nods at everyone.

BIL just played the "are you married" card. This is escalating. Manu's sense of husbandly empathy has been invoked.

It turns out Manu is indeed married. BIL is visibly relieved.

Lorry Driver wants them both to know that he too is married.

In a tragic twist, Lorry Drivers marriage was not deemed worthy of discussion by anyone. Lorry Driver is now my rooting interest

It appears Manu is brokering some sort of compromise.

Apparently compromise is that if BIL buys some sacks of rice* and then Manu will make the rest just go away.

*Number under negotiation

Manu has opened aggressively with a you take half I take half offer. BIL has counetered by pointing out in that case Manu will need to take him too

BIL is now saying he can do 10 bags but does Manu want a bottle of scotch thrown in? I deeply admire this man's commitment to corruption.

Plot twist: Manu is a teetotaller apparently

The lorry driver has shared that he however, would rather like a bottle of whisky. He is also willing to accept rum. He's accomodating like that.

Manu has informed him he won't be getting anything of the sort. Lorry driver looks unhappy

Lorry driver is no longer speaking up when Manu wants him to chime in. Heel turn.

BIL just produced a MS Dhoni/Tom Brady level comeback and has sent for rum for lorry driver. He is exploiting the breach.

Meanwhile mom wants to go to bed and I need to convince her not to she is our only window into this ricely saga send thoughts and prayers

Update: Mom is not going to bed just yet, I invoked this ridiculously large audience and it swayed her.

I think she may be judging y'all for caring this much about rice, but she's been judging me my whole life too, you'll be fine

Neighbour Uncle has emerged wearing kurta pajama. He wants to solve the problem himself.

Neighbour Uncle has unemerged because he was not wearing a mask and Neighbour Aunt was shouting at him

Meanwhile BIL and Manu seem to be closing in on a deal in the 20-25 bag range. Lorry Driver is now not even trying to hide his alignment switch.

They are now shaking hands. I believe we may have an accord.

Final terms: 23 bags, one bottle Old Monk, one bottle scotch*. Everyone is exhausted. 

* Lorry driver is the best fucking negotiator of the lot

ITS NOT OVER OH GOD NOW WHO WILL UNLOAD 23 BAGS ARGUMENT HAS STARTED

Lorry driver is sick of this shit. He has told helper to unload bags.

Helper, LD and BIL are now unloading bags. This will take a while.

Manu's work is done. He is leaving. This is not the only crisis he needs to solve tonight, no doubt. No rest for the elite specialist

Neighbour Uncle has re-emerged, now wearing mask.

BIL just asked Neighbour Uncle to help with bags.  I don't think I've ever seen a senior citizen walk home that fast.

Correction: He is not a senior citizen apparently. My mistake.
"""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
