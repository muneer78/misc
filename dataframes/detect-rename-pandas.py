import os
import pandas as pd
from textblob import TextBlob


# Function to detect English words in a string and return them separated by underscores
def detect_english_words(text):
    blob = TextBlob(text)
    words = [word for word in blob.words if word.isalpha()]
    return "_".join(words)


csv_name = r"C:\Users\mahmad\OneDrive - Ryan RTS\Code\renames.csv"
# parent_dir is the directory that has the folders you want to rename
parent_dir = r"C:\Users\mahmad\OneDrive - Ryan RTS\Code\localwork"
df = pd.read_csv(csv_name)

# Detect English words in the 'old' column and create a new column with the results
df["new"] = df["old"].astype(str).apply(detect_english_words)

list_oldnames = df["old"].astype(str).to_list()
list_newnames = df["new"].astype(str).to_list()

for folder in os.listdir(parent_dir):
    for oldname, newname in zip(list_oldnames, list_newnames):
        if str(oldname) == str(folder):
            try:
                os.rename(
                    os.path.join(parent_dir, oldname), os.path.join(parent_dir, newname)
                )
            except Exception as e:
                print(f"Could not rename {os.path.join(parent_dir, oldname)}: {e}")

# Save the updated DataFrame to a new CSV file
df.to_csv("updated_renames.csv", index=False)

print("English words detected and used as new filenames in 'updated_renames.csv'.")
