from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
nltk.download('punkt')

def summarize_paragraph(paragraph, sentences_count=2):
    parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))

    summarizer = LsaSummarizer(Stemmer("english"))
    summarizer.stop_words = get_stop_words("english")

    summary = summarizer(parser.document, sentences_count)
    return summary

if __name__ == "__main__":
    article = """One thing that sometimes happens is that an activist hedge fund will quietly accumulate a stake in a public company, and then it will announce its position and push for changes at the company. Often the company’s stock will go up when the activist announces its position, since the activist often (1) has a good track record and/or (2) targets a company that could use a bit of a managerial shake-up. Often, too, the company’s board of directors will come out against the activist when it announces its position: The board presumably likes the current strategy and will feel blindsided and aggrieved to be targeted by the activist.

Boards really do get stressed about this, so there is a whole activism-defense industry of people whose job is to prepare boards of directors for activist attacks: There are best practices to insulate your company against activists, good ways to respond if an activist shows up, etc. Activism defense also tries to do early warning: Even before the activist publicly discloses its stake, or calls the board up privately to push for changes, there might be signs (rumors, trading volumes, etc.) that an activist might be buying the stock, and the board might be alerted to those signs so it can be ready to fight the activist threat as soon as it materializes.

If you are a director on the board of a company with a lurking activist, what should you do about it? There are various imaginable corporate-finance and public-relations moves you can make, but there is also a simple personal finance move, which is: Buy more stock? Not legal or investing advice, but here’s “Betting on my enemy: Insider trading ahead of hedge fund 13D filings,” by Truong Duong, Shaoting Pi and Travis Sapp in the Journal of Corporate Finance:

    Corporate insiders often become aware of hedge fund attention prior to a 13D filing. We find abnormal buying activity by insiders in the months leading up to hedge fund 13D filings. Whereas 13D announcement abnormal returns are 7.72 %, profits to insiders who buy average 12.09 %. Insider buying is not linked to common firm characteristics that predict activist targeting. Our findings indicate that insiders are benefiting from private knowledge that their firm has become the focus of hedge fund activism, and sometimes this knowledge comes directly from the activist. However, insiders largely refrain from trading when there is formal communication with the activist. Profits to insiders who buy when there are no talks prior to the 13D filing are 14.49 %, triple the amount for insiders who have had early talks with the hedge fund. Insider trading is linked to indicators of poor corporate culture, but not related to outcomes of activism campaigns.

On the one hand, if the insiders are buying stock to bet on the activist, that somewhat undermines their defense against that activist. But I suppose it’s a good hedge. If an activist is buying your stock, one possible outcome is that the activist will run a proxy fight and you will be kicked off the board. That would be bad for you, but in that case, the stock that you bought will probably be up, which will be some consolation."""

sentences_count = 6
summary = summarize_paragraph(article, sentences_count)

for sentence in summary:
    print(sentence)

with open('article.md', 'w') as f:
    f.write("# Article Summary\n\n")
    for summary in article:
        f.write(summary + "\n")

print("Summary written to article.md")