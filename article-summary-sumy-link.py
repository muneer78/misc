from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import textwrap
import requests
from bs4 import BeautifulSoup

nltk.download("punkt")


def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    return "\n\n".join(paragraphs)


def summarize_paragraph(paragraph, sentences_count=2):
    parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
    summarizer = LsaSummarizer(Stemmer("english"))
    summarizer.stop_words = get_stop_words("english")
    summary = summarizer(parser.document, sentences_count)
    return summary


if __name__ == "__main__":
    url = "https://www.gelliottmorris.com/p/the-myth-of-republican-isolationism"
    article = extract_text_from_url(url)
    sentences_count = 6
    summary = summarize_paragraph(article, sentences_count)

    print("# Article Summary\n")
    for sentence in summary:
        wrapped = textwrap.fill(str(sentence), width=80)
        print(wrapped)
