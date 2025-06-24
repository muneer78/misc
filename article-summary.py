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
    article = """Sell-side research analysts are unusual in that they are white-collar knowledge workers whose work quality is (1) public and (2) objectively measurable. Research analysts publish reports telling you what stocks to buy and sell, with price targets and estimates of future earnings; plausibly the best analysts are the ones whose recommendations, price targets and earnings estimates most accurately predict future stock prices and earnings. [3]  Also they’re mostly on LinkedIn. So you can ask questions like “which characteristics make an analyst good,” and use publicly available information to get answers that are (1) plausibly true and (2) plausibly generalizable to other sorts of white-collar knowledge workers.

This leads to a lot of academic studies of research analysts. We have discussed a paper examining analysts’ taxi trips to visit companies (result: an analyst who visits a company before it reports earnings will tend to have a good earnings estimate), and another one examining analysts who have the same first name as the chief executive officers of the companies they cover (result: also good for estimate accuracy). 

Covid-19 provided a series of natural experiments for this sort of study: When Covid-19 hit, many white-collar workers worked from home for a while, and then companies mostly required them to return to the office, but some companies were more or less strict about that and there was sort of random selection of who had to go back to the office and when. Perhaps white-collar work is improved by working from home: Perhaps people are more creative, less distracted, less stressed, less susceptible to groupthink, have more time to work without having to commute. Or perhaps it is improved by working from the office: Perhaps people are less diligent, less collaborative, less connected to their work and their colleagues and their customers.

And one way to find out is of course to look at analysts’ earnings estimates. Here’s “The Impact of Return-to-Office Mandates on Equity Analysts,” by Peixin Li, Baolian Wang and Jiawei Yu, which finds “that RTO mandates significantly enhance forecast accuracy,” reducing earnings forecast errors by about 15% and also improving “forecast timeliness.” Also:

    Forecast accuracy gains are greater for younger, less experienced analysts, consistent with the notion that WFH deprives them of critical mentoring opportunities. Female analysts exhibit larger accuracy improvements than their male counterparts, possibly due to greater domestic distractions during WFH. Third, RTO mandates have a more pronounced impact on analysts' first forecasts issued after earnings announcements compared to other forecasts. This is consistent with the understanding that analysts are generally expected to release updated forecasts within a few days of earnings announcements, often under heightened time pressure. Fourth, the effects are stronger for analysts based in Democratic-leaning states than in Republican-leaning states. One possible explanation is that analysts in Republican states were already more inclined to voluntarily work in the office prior to the imposition of formal RTO mandates, thereby dampening the marginal effect of such mandates.

    These findings suggest that RTO entails productivity gains, suggesting that WFH is associated with increased distractions or diminished collaboration efficacy

Also “RTO effects concentrate on stocks that are less important to analysts’ careers (e.g., those with smaller market capitalization, lower trading volume, or lower institutional ownership),” suggesting that the analysts were able to focus on the most important parts of their jobs from home, but at the office they have to do all the other parts of their jobs too."""

sentences_count = 6
summary = summarize_paragraph(article, sentences_count)

for sentence in summary:
    print(sentence)

with open('article.md', 'w') as f:
    f.write("# Article Summary\n\n")
    for summary in article:
        f.write(summary + "\n")

print("Summary written to article.md")