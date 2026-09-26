import os
import pandas as pd


csv_name = r"C:\Users\mahmad\OneDrive - Ryan RTS\Code\renames.csv"
# parent_dir is the directory that has the folders you want to rename
parent_dir = r"C:\Users\mahmad\OneDrive - Ryan RTS\Code\utils\utils"
df = pd.read_csv(csv_name)

list_oldnames = df["old"].astype(str).to_list()

list_newnames = df["new"].astype(str).to_list()

for folder in os.listdir(parent_dir):
    for oldname, newname in zip(list_oldnames, list_newnames):
        if str(oldname) == str(folder):
            try:
                os.rename(
                    os.path.join(parent_dir, oldname), os.path.join(parent_dir, newname)
                )
            except:
                print("Could not rename " + str(os.path.join(parent_dir, oldname)))
