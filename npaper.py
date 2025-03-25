import newspaper
import os

url = 'http://www.newyorker.com/reporting/2009/10/26/091026fa_fact_goodyear?printable=true'

# Extract web data
url_i = newspaper.Article(url="%s" % (url), language='en')
url_i.download()
url_i.parse()

filename = input("Input the Filename: ")

# Display and write scrapped data
with open(filename, mode="w") as f:
	print(url_i.text, file=f)