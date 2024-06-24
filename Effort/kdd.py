from flask import Flask, render_template, request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)

# Example of a rule-based summarization function (you can replace this with your own implementation)
def rule_based_summarizer(article, num_sentences):
    # Implement your rule-based summarization logic here
    # For example, extract first few sentences or sentences containing specific keywords
    sentences = article.split(".")  # Split into sentences (naive approach)
    summary = ". ".join(sentences[:num_sentences])  # Take specified number of sentences as summary
    return summary

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    article = request.form["article"]
    summarization_size = request.form["summarization_size"]

    # Using sumy for extractive summarization
    parser = PlaintextParser.from_string(article, Tokenizer("english"))
    summarizer = LsaSummarizer()

    if summarization_size == "small":
        summary_size = 3
    elif summarization_size == "medium":
        summary_size = 5
    elif summarization_size == "large":
        summary_size = 10
    else:
        summary_size = 5  # Default to medium if size is not specified

    summary_sumy = summarizer(parser.document, summary_size)

    # Format sumy summary into a single string
    summarized_text_sumy = ""
    for sentence in summary_sumy:
        summarized_text_sumy += str(sentence) + " "

    # Rule-based summarization
    summary_rule_based = rule_based_summarizer(article, summary_size)

    return render_template("summary.html", article=article, summary_sumy=summarized_text_sumy, summary_rule_based=summary_rule_based)

if __name__ == '__main__':
    app.run(debug=True)
