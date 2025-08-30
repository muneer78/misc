### Read CSV file of URLs
import csv
with open('links.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
 
### Perform a while loop until a row is null
# Extract main body text from URL
# justext piece
 
### Store name of URL as variable 1
import os
from urllib.parse import urlparse
 
url = 'http://example.com/somefile.zip'
urlparse.urlsplit(url).path.split('/')[-1]
 
### Store name of URL as variable 2
import posixpath
import urlparse
 
path = urlparse.urlsplit(URL).path
filename = posixpath.basename(path)
 
### Store name of URL as variable 3
>>> remotefile=urllib2.urlopen(url)
>>> try:
>>>   filename=remotefile.info()['Content-Disposition']
>>> except KeyError:
>>>   filename=os.path.basename(urllib2.urlparse.urlsplit(url).path)
 
### Store page name as variable
import urllib.request as urllib
from bs4 import BeautifulSoup
soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
print soup.title.string
 
### Write the result to a text file using the naming convention [URL Name].txt
filename = "simple" + str(minLength) + str(minBF) + ".csv"
resfile = open(filename,"w")
 
### Write the result to a text file using the naming convention [Page Name].txt
filename = ### Write the result to a text file using the naming convention [URL Name].txt
filename = "soup.title.string + ".txt"
resfile = open(filename,"w")