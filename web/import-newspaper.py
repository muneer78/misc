import newspaper
import os
import csv
import requests

# Extract web data
url_i = newspaper.Article(url="%s" % (url), language='en')
url_i.download()
url_i.parse()

# Display and write scrapped data
file= open('url.csv', "r")
    reader = csv.reader(file)
    for row in reader:
        urls = row[0]
        print (urls)
        r = requests.get(urls)