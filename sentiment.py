import glob
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    return score


files = glob.glob("dados\\believes\\*.json")
for filename in files:
    with open(filename, 'r', encoding="utf8") as f:
        print(filename)
        data = json.load(f)

        for item in data:
            score = sentiment_analyzer_scores(data[item]["text"])
            data[item]['sentiment'] = score['compound']

    with open(filename, 'w', encoding="utf8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
