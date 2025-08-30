import csv
import requests

file= open('url.csv', 'rb')fgfgfgf
    reader = csv.reader(f)
    for row in reader:
        urls = row[0]
        print (urls)
        r = requests.get(urls)