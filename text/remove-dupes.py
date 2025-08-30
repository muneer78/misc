# Input string
input_string = """133853MASTER
150799MASTER
136995MASTER
148044MASTER
136995MASTER
127093REC
142811REC
108199REC
119500MASTER
130357REC
102624REC
126677REC
143048REC
148671MASTER
141114REC
104276REC
100523REC
115229REC
105999NONREC
131287MASTER
103955REC
150595MASTER
104529REC
150727MASTER
149612MASTER
123942MASTER
150727MASTER
126482MASTER
125342MASTER
150595MASTER
148647MASTER
150866MASTER
150971MASTER
103634MASTER
137620REC
133869REC
131086REC
138896REC
148446MASTER
111038REC
123942MASTER
105251REC
131460REC
101354REC
136653MASTER
150977MASTER
106382REC
127260REC
141482REC
149612MASTER
139493REC
148647MASTER
101657REC
131287MASTER
136653MASTER
103634MASTER
103634MASTER
150918MASTER
150977MASTER
136995MASTER
150918MASTER
148044MASTER
105581REC
134566REC
126482MASTER
125342MASTER
144463REC
139619REC
123271REC
125615REC
141177REC
102641REC
135045REC
146134MASTER
148671MASTER
150976MASTER
131287MASTER
119500MASTER
119500MASTER
128046REC
136913REC
140716REC
144272REC
145940MASTER
148446MASTER
145940MASTER
146134MASTER
101283REC
132344REC
133853MASTER
150976MASTER
150799MASTER
136217NONREC
136456REC
150866MASTER
150971MASTER
106459REC
104136REC
106509REC
134577REC
102336REC"""

# Split the string into a list of words
words = input_string.split("\n")

# Initialize a set to keep track of seen words and a list for removed duplicates
seen = set()
removed_duplicates = []

# Use OrderedDict to remove duplicates while preserving order
unique_words = []
for word in words:
    if word not in seen:
        seen.add(word)
        unique_words.append(word)
    else:
        removed_duplicates.append(word)

# Join the unique words back into a single string with each word on a new line
output_string = "\n".join(unique_words)

# Print the unique words, the removed duplicates, and their counts
print("Unique records:")
print(output_string)
print(f"\nCount of unique records: {len(unique_words)}")

print("\nRemoved duplicates:")
print("\n".join(removed_duplicates))
print(f"\nCount of removed duplicates: {len(removed_duplicates)}")
