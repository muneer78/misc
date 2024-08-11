import pyperclip

def add_gt_in_front_of_paragraphs(text):
    # Split the text into paragraphs based on double newline
    paragraphs = text.split('\n\n')

    # Add '> ' in front of each paragraph
    updated_paragraphs = [f'> {paragraph.strip()}' for paragraph in paragraphs]

    # Join the paragraphs back with double newline
    updated_text = '\n\n'.join(updated_paragraphs)

    return updated_text

# Sample input text
input_text = """Hello again! I'm sorry if this is hard to follow English isn't my first language.

So to recap I (M19) got my brother (M25) a new car. My brother sacrificed his entire life so he could raise my siblings and I. He worked multiple jobs so he could pay for rent, give us food and get us into the sports we wanted. He gave up a scholarships because he wanted to stay near us so we wouldn't have to go into the system like he did. I am m the youngest out of my siblings and moved out for college so he is basically done raising us. I had an idea with my brother (M20) to get him a new car. Since his is really old and run down. I got him a 2020 Audi and it was pretty cheap since a guy from my internship sold it to me.

When I showed him the new car, my brother just stood there in disbelief and said "what the fuck is this for?" I tried to explain to him that he deserves it after everything he has done us.

He said "I get the sentiments but I'm not your dad. I don't wanna be a dad. I just wanna move on okay? I don't deserve a standing ovation because I did what every single "parent" every single day without complaint I signed up to be your guardian because I love you and you deserve a good life. Not because I wanted to live off your success and money. If you want the car then keep it but it's not mine. I have a car." And he stormed off before I could say anything else.

A lot of you gave me amazing and reasonable advice. One of them was giving him some space so he could cool off for a little bit and that's what I did. We only texted so he could check in on me but that's pretty the extent of our conversations.

Today I called him and asked him if we could meet at a dinner so we could talk and he agreed.

At first there was just silence and he broke it by saying " look I'm gonna address the elephant in room, I'm so sorry for snapping at you, it was underserved and you deserve a better old brother. And I'm so sorry for all the times that I was angry, stressed and moody. You deserves better, I wish I could back in time and give you a better childhood but I can't. I'm so sorry for treating your gift like that, it's just that, I need you to understand that what I did wasn't special, I just wanna move on. Please don't think that because you're an amazing success now that means that you owe it to me.

You don't. It's all your hard work, staying up late studying, all the times you could've gone out partying you spent working at school. I wanna stess that I didn't do it so you have to owe me something. I did it because you guys are great kids and you deserve and are owed a great life. I wish I could've done more but I did my best and I'm so sorry if I've ever said or did anything to make you feel like you owe me. You don't. I want to live your life. I'm not your dad. Okay? Do you understand that? I just wanna be me now" He started to get choked up and turned his head away from me.

I told him that; "I know that you love me. person who doesn't love you wouldn't ever take care of me the way you do. Just like I could've gone out partying instead of studying, you could've left and moved on with your life with that scholarship, never look back and let the system take us. But you didn't. It was never your responsibility to take care of us. It's understandable that you were stressed and angry. You were a child yourself. You need to give yourself grace and mercy.

I gave you that gift because I want your life to be easier and let's face it, the car you have is a safety issue. You've been working since you were seven. It's okay to take it easy now. You've lived the life, had the responsibilities and had the stress of someone three times your age. It's okay that you take it easy and rest because that's what you're supposed to do. If you don't rest and we need you, you won't be at 100%. You take care of anyone if you don't take care of yourself.

I understand that you wanna be you and whatever you need to me or any of us to do to get you there to back to yourself. We will do it. I know you're not my dad but I need you to understand that you're not because everything you did was the embodiement selflessness. You deserve that car and more."

He let out sigh and said "I don't even know who the fuck I am. All I know is that I don't want kids because I'm not doing this shit all over again"

I nodded and said "I get that. I wouldn't know how I am outside of taking care of people either especially if I've been doing my entire life but you can start now. I want that for you."

He told me that he'll take car if the offer is still on table and I'm gonna drop it off for him tomorrow. We both promised to work on having more of a brotherly relationship between us and he promised to try and find out who he is.

Thank you so much for reading and I really appreciate your help. Thank you again I really can't stress it enough"""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
