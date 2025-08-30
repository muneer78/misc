import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
import textwrap

nlp = spacy.load("en_core_web_sm")


def summarize_paragraph(paragraph, sentences_count=3):
    doc = nlp(paragraph)
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ["PROPN", "ADJ", "NOUN", "VERB"]
    for token in doc:
        if token.text in stopwords or token.text in punctuation:
            continue
        if token.pos_ in pos_tag:
            keyword.append(token.text)
    freq_word = Counter(keyword)
    if not freq_word:
        return ""
    max_freq = freq_word.most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = freq_word[word] / max_freq
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                sent_strength[sent] = sent_strength.get(sent, 0) + freq_word[word.text]
    summarized_sentences = nlargest(
        sentences_count, sent_strength, key=sent_strength.get
    )
    final_sentences = [sent.text.strip() for sent in summarized_sentences]
    summary = "\n".join(final_sentences)
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

    print("\n# Article Summary\n")
    for sentence in summary.split("\n"):
        wrapped = textwrap.fill(sentence, width=80)
        print(wrapped)
