import os
import unicodecsv as csv

# open and store the csv file
IDs = {}
with open("data.csv", "rb") as csvfile:
    timeReader = csv.reader(csvfile, delimiter=",")
    # build dictionary with associated IDs
    for row in timeReader:
        IDs[row[0]] = row[1]
# move files
path = "/Users/muneer78/Desktop/books"
tmpPath = "/Users/muneer78/Desktop/books01"
for oldname in os.listdir(path):
    # ignore files in path which aren't in the csv file
    if oldname in IDs:
        try:
            os.rename(os.path.join(path, oldname), os.path.join(tmpPath, IDs[oldname]))
        except:
            print("File " + oldname + " could not be renamed to " + IDs[oldname] + "!")
