import requests
import time
import argparse
import datetime
from shutil import copyfile
import os

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
            url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=ERO5XRBZNWQ9E608".format(
                args.symbol), headers=headers)
        data = resp.json()
        print("Data: " + str(data))
        companyTicker = data['Meta Data']['2. Symbol']
        print(companyTicker)
        #print(data[1]["4. close"])
        stockPrice = extract_values(data, "4. close")
        #stockPrice = data['Time Series (5min)']['4. close']
        print(stockPrice[0])
        time.sleep(20)
        # Query for the stock name, for refined news queries.
        resp = requests.get(
            url="https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey=ERO5XRBZNWQ9E608".format(
                args.symbol), headers=headers)
        data = resp.json()
        # print(data)
        # time.sleep(20)
        companyName = data['bestMatches'][0]['2. name']
        print("Company Name: " + companyName)

        # Query for news
        resp = requests.get(
            url='https://newsapi.org/v2/everything?'
                'q={}&'
                'from=2020-02-02'  # This is the OLDEST date an article can be from, free edition will let you have a month
                'sortBy=popularity&'  # Filter by popularity
                'apiKey=677a8a1783e242b08e908b272fed2e4f'.format(
                args.symbol + " " + companyName),
            headers=headers)  # Adds the company name in full after the ticker, for more accurate news queries
        print(resp)
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
        if positive > negative and hold > positive:
            aggregate = "Hold -> Buy"
        if negative > positive and hold > negative:
            aggregate = "Hold -> Sell"

        print("\n\nPositive Analysis: " + str(positive) + ",\nNegative Analysis: " + str(
            negative) + ",\nHold Analysis: " + str(hold))
        print(
            "\n\nStock Analysis: " + companyTicker + ",\nPrice: " + stockPrice + ",\nAggregate: " + aggregate + ",\nTimestamp: " + str(
                int(time.time())) + "\n")  # unix timestamp

        # Prevent throttling. Can make one request per 172.8 seconds as I have 500 requests a day.
        time.sleep(10)
    except Exception as e:
        print("Error: " + str(e))
        time.sleep(10)

