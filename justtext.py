import requests
import justext

response = requests.get("https://www.si.com/more-sports/2008/12/03/dave-kingman")
paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
with open("kingman.txt", "a") as f:
	for paragraph in paragraphs:
		if not paragraph.is_boilerplate:
			print (paragraph.text, file=f)
			


