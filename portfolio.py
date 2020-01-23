import requests
import time
import datetime
from shutil import copyfile
import os

while True:
    articleCount = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    with open("stocks.txt", "r") as ins:
        for line in ins:
            ticker = line

            positive = 0
            hold = 0
            negative = 0
            aggregate = "Insufficient Data"

            try:
                #Query stock information, price etc.
                resp = requests.get(
                    url="https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols={}&apikey=ERO5XRBZNWQ9E608".format(
                        ticker), headers=headers)
                data = resp.json()
                #print(data)
                #time.sleep(20)
                companyTicker = data['Stock Quotes'][0]['1. symbol']
                stockPrice = data['Stock Quotes'][0]['2. price']

                #Query for the stock name, for refined news queries.
                resp = requests.get(
                    url="https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey=ERO5XRBZNWQ9E608".format(
                        ticker), headers=headers)
                data = resp.json()
                #print(data)
                #time.sleep(20)
                companyName = data['bestMatches'][0]['2. name']
                print("Company Name: " + companyName)

                #Query for news
                resp = requests.get(
                        url='https://newsapi.org/v2/everything?'
                        'q={}&'
                        'from=2019-11-04' # This is the OLDEST date an article can be from, free edition will let you have a month
                        'sortBy=popularity&' #Filter by popularity
                        'apiKey=***********************'.format(
                        ticker + " " + companyName), headers=headers) #Adds the company name in full after the ticker, for more accurate news queries
                data = resp.json()
                #print(data)
                #time.sleep(20)

                for article in data['articles']:
                    articleCount = articleCount + 1
                    newsUrl = article['url']
                    print(newsUrl)
                    resp = requests.get(url=newsUrl, headers=headers, timeout=10)
                    data = resp.text

                    data.lower()
                    #Checks to ensure news is relevant, and contains or mentions the stock
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

                print("\n\nPositive Analysis: " + str(positive) + ",\nNegative Analysis: " + str(negative) + ",\nHold Analysis: " + str(hold)) 
                print("\n\nStock Analysis: " + companyTicker + ",\nPrice: " + stockPrice + ",\nAggregate: " + aggregate + ",\nTimestamp: " + str(int(time.time())) + "\n") #unix timestamp

                # Prevent throttling. Can make one request per 172.8 seconds as I have 500 requests a day.
                time.sleep(10) 
            except Exception as e:
                print("Error: " + str(e))
                time.sleep(10)
