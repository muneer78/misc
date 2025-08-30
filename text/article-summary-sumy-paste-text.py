from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import textwrap


def summarize_paragraph(paragraph, sentences_count=3):
    parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
    summarizer = LsaSummarizer(Stemmer("english"))
    summarizer.stop_words = get_stop_words("english")
    summary = summarizer(parser.document, sentences_count)
    return summary


if __name__ == "__main__":
    print("Paste your article text below. Enter a blank line to finish:\n")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    article = "\n".join(lines)
    sentences_count = 6
    summary = summarize_paragraph(article, sentences_count)

    with open("article.md", "w") as f:
        f.write("# Article Summary\n\n")
        print("# Article Summary\n")
        for sentence in summary:
            wrapped = textwrap.fill(str(sentence), width=80)
            print(wrapped)
            f.write(wrapped + "\n")

    print("Summary written to article.md")
