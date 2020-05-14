import requests
import time
import argparse
import sys
import datetime
import passwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

date_sentiments = {}

# New key words and values
key_words = {
    'crushes': 10,
    'buy': 10,
    'beats': 5,
    'purchase': 10,
    'pay attention': 5,
    'should invest': 20,
    'long': 15,
    'outperform': 20,
    'upgrade': 15,
    'increased target': 20,
    'bullish': 10,
    'bull': 5,
    'hold': -5,
    'holds': -5,
    'misses': -10,
    'sell': -20,
    'avoid': -10,
    'should not invest': -50,
    'short': -20,
    'downgrade': -10,
    'trouble': -10,
    'decreased target': -20,
    'bearish': -10,
    'bear': -10,
    'sink': -30,
    'falls': -100,
}

# Instantiate the sentiment intensity analyzer with the existing lexicon
vader = SentimentIntensityAnalyzer()

# Update the lexicon
vader.lexicon.update(key_words)


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


parser = argparse.ArgumentParser(description="A tutorial of argparse!")
parser.add_argument("--symbol", required=True, type=str, help="The companies symbol, i.e INTC")
args = parser.parse_args()

while True:
    articleCount = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 '
                      'Safari/537.36 '
    }
    positive = 0
    hold = 0
    negative = 0
    aggregate = "Insufficient Data"

    try:
        # Query stock information, price etc.
        resp = requests.get(
            url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(
                args.symbol, passwords.alphaAPI), headers=headers)
        data = resp.json()
        # print("Data: " + str(data))
        companyTicker = data['Meta Data']['2. Symbol']
        print(companyTicker)
        # print(data[1]["4. close"])
        stockPrice = extract_values(data, "4. close")
        print(stockPrice[0])
        # time.sleep(20)
        # Query for the stock name, for refined news queries.
        resp = requests.get(
            url="https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}".format(
                args.symbol, passwords.alphaAPI), headers=headers)
        data = resp.json()
        # print(data)
        # time.sleep(20)
        companyName = data['bestMatches'][0]['2. name']
        print("Company Name: " + companyName)
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        print(yesterday)
        # Query for news
        resp = requests.get(
            url='https://newsapi.org/v2/everything?'
                'q={}&'
                'from={}'  # This is the OLDEST date an article can be from, free edition will let you have a month
                'sortBy=popularity&'  # Filter by popularity
                'apiKey={}'.format(
                args.symbol + " " + companyName, yesterday, passwords.newsAPI),
            headers=headers)  # Adds the company name in full after the ticker, for more accurate news queries
        data = resp.json()
        # print(data)
        # time.sleep(20)

        for article in data['articles']:
            articleCount = articleCount + 1
            newsUrl = article['url']
            print(newsUrl)
            resp = requests.get(url=newsUrl, headers=headers, timeout=10)
            data = resp.text

            data.lower()
            # Checks to ensure news is relevant, and contains or mentions the stock
            if data.count("stock") > 0 or data.count("shares") > 0:
                if data.count(companyTicker) > 0 or data.count(companyName) > 0:
                    sentiment = vader.polarity_scores(data)['compound']
                    print("sentiment = " + str(sentiment))
                    # date_sentiments.setdefault(date, []).append(sentiment)
                    # logically NLP semantic analysis should take place here
                    positive = positive + data.count("buy")
                    positive = positive + data.count("purchase")
                    positive = positive + data.count("pay attention")
                    positive = positive + data.count("should invest")
                    positive = positive + data.count("long")
                    positive = positive + data.count("outperform")
                    positive = positive + data.count("upgrade")
                    positive = positive + data.count("increased target")
                    positive = positive + data.count("bullish")
                    positive = positive + data.count("bull")

                    hold = hold + data.count("hold")
                    hold = hold + data.count("market perform")

                    negative = negative + data.count("sell")
                    negative = negative + data.count("avoid")
                    negative = negative + data.count("should not invest")
                    negative = negative + data.count("short")
                    negative = negative + data.count("downgrade")
                    negative = negative + data.count("decreased target")
                    positive = positive + data.count("bearish")
                    positive = positive + data.count("bear")
                    positive = positive + data.count("sink")

        if positive > hold and positive > negative:
            aggregate = "Buy"
        if negative > positive and negative > hold:
            aggregate = "Sell"
        if positive == negative and hold == positive and hold == negative:
            aggregate = "Hold"
        if negative < positive < hold:
            aggregate = "Hold -> Buy"
        if positive < negative < hold:
            aggregate = "Hold -> Sell"

        print("\n\nPositive Analysis: " + str(positive) + ",\nNegative Analysis: " + str(
            negative) + ",\nHold Analysis: " + str(hold))
        print(
            "\n\nStock Analysis: " + str(companyTicker) + ",\nPrice: " + str(stockPrice[0]) + ",\nAggregate: " + str(
                aggregate) + ",\nTimestamp: " + str(
                int(time.time())) + "\n")  # unix timestamp
        print("Time : " + str(datetime.datetime.now()))

        # Prevent throttling. Can make one request per 172.8 seconds as I have 500 requests a day.
        # time.sleep(10)

    except Exception as e:
        print("Error: " + str(e))
        time.sleep(10)

    sys.exit()
