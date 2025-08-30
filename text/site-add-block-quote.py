import pyperclip


# Use if blank lines also need to be block quoted
def add_gt_in_front_of_paragraphs(text):
    # Split the text into lines
    lines = text.split("\n")

    # Add '> ' in front of each line, including blank lines
    updated_lines = [f"> {line}" if line.strip() else "> " for line in lines]

    # Join the lines back with newline
    updated_text = "\n".join(updated_lines)

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
    updated_text = "\n".join(updated_lines)

    return updated_text


# Sample input text
input_text = """
Robert Adolph Boehm, in accordance with his lifelong dedication to his own personal brand of decorum, muttered his last unintelligible and likely unnecessary curse on October 6, 2024, shortly before tripping backward over "some stupid mother****ing thing" and hitting his head on the floor.

Robert was born in Winters, TX, to the late Walter Boehm and Betty Smith on May 6, 1950, after which God immediately and thankfully broke the mold and attempted to cover up the evidence. Raised Catholic, Robert managed to get his wife Dianne pregnant (three times) fast enough to just barely miss getting drafted into the Vietnam War by fathering Michelle, John, and Charlotte between 1967 and 1972. Much later, with Robert possibly concerned about the brewing conflict in Grenada, Charles was born in 1983.

This lack of military service was probably for the best, as when taking up shooting as a hobby in his later years, he managed to blow not one, but two holes in the dash of his own car on two separate occasions, which unfortunately did not even startle, let alone surprise, his dear wife Dianne, who was much accustomed to such happenings in his presence and may have actually been safer in the jungles of Vietnam the entire time.

While the world was in conflict elsewhere, Robert made due by learning to roof, maintain traffic signs with the City of Amarillo, and eventually becoming a semi-professional truck driver—not to be confused with a professional semi-truck driver.

With peace on the horizon, Robert's attention somewhat counterintuitively drifted to weapons of war, spanning the historical and geographical spectrum from the atlatl of 19,000 BC France, to the sjambok of 1830s Africa, to the Mosin-Nagant M1891 of WWII-era Soviet Union. So many examples of these mainstream hobbyist items litter his small Clarendon, Texas, apartment that one of them may very well have been the item referenced in his aforementioned eloquent final epitaph.

A man of many interests, Robert was not to be entranced by historical weapons alone, but also had a penchant for fashion, frequently seen about town wearing the latest trend in homemade leather moccasins, a wide collection of unconventional hats, and boldly mismatched shirts and pants.

Robert also kept a wide selection of harmonicas on hand—not to play personally, but to prompt his beloved dogs to howl continuously at odd hours of the night to entertain his many neighbors, and occasionally to give to his many, many, many grandchildren and great-grandchildren to play loudly during long road trips with their parents.

Earlier this year, in February, God finally showed mercy upon Dianne, getting her the hell out of there for some well-earned peace and quiet. Without Dianne to gleefully entertain, Robert shifted his creative focus to the entertainment of you, the fine townspeople of Clarendon, Texas. Over the last eight months, if you have not met Robert or seen his road show yet, you probably would have soon.

We have all done our best to enjoy/weather Robert's antics up to this point, but he is God's problem now.

Robert's farewell tour will be held Monday, October 14th, at 10 a.m. at Memorial Park Funeral Home, 6969 E Interstate 40 Hwy, Amarillo, TX 79118. The family encourages you to dust off whatever outdated or inappropriate combination of clothing you have available to attend. A tip jar will be available in the front; flowers are also acceptable.
"""

# Apply the function to the input text
output_text = add_gt_in_front_of_paragraphs(input_text)

# Copy the updated text to the clipboard
pyperclip.copy(output_text)

print("The updated text has been copied to the clipboard.")
