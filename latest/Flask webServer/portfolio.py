import requests
import time
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from joblib import dump, load
import json

articles = []
resultsPos = []
resultsNeg = []
prediction = []
news = ""
overall = 0;

def JSON():
    return my_json_string

def newsJSON():
    return news

with open(f'model/newsSentiment.joblib', 'rb') as f:
   model = load(f)


def test():
    return articles


def prediction():
    return prediction


articleCount = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

with open("stocks.txt", "r") as ins:
    count = 1
    for line in ins:
        ticker = line
        aggregate = "Insufficient Data"

        try:
            # Query for the stock name, for refined news queries.
            resp = requests.get(
                url="https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey=ERO5XRBZNWQ9E608".format(
                    ticker), headers=headers)
            data = resp.json()
            #print(data)
            companyName = data['bestMatches'][0]['2. name']
            print("Parsing news for : " + companyName)



            #Query for news
            resp = requests.get(
                url='https://newsapi.org/v2/everything?'
                    'q={}&'
                    'from=2020-04-05' # This is the OLDEST date an article can be from, free edition will let you have a month I believe
                    'sortBy=popularity&' #Filter by popularity (read the newsapi docs)
                    'apiKey=fe00115ceffe418988616191b03e1c74'.format(
                    ticker + " " + companyName), headers=headers) #Add the company name in full after the ticker, for more accurate news queries
            data = resp.json()

            for article in data['articles']:
                articleCount = articleCount + 1
                newsUrl = article['url']
                #print(newsUrl)
                newsArticle = article['title']
                articles.append(newsArticle)
                #print(newsArticle)

            #print("Stock Analysis: " + ticker +  "," + aggregate + "," + str(int(time.time()))) #unix timestamp at the end

            # Prevent throttling. Can make one request per 172.8 seconds as we have 500 requests a day.
            time.sleep(10) #Should be 173 seconds but we don't have time for that

        except Exception as e:
            print("Error: " + str(e))
            time.sleep(10)

    ins.close();



# Create the pandas DataFrame
df = pd.DataFrame({'headlines': articles})
news = df.to_json(orient='index')
#df.to_json(r'model/exportedNews.json', orient='split')

fresh_news = df;
vectorizer_new_data = CountVectorizer(max_features=30, min_df=9)
processed_features_new_data = vectorizer_new_data.fit_transform(fresh_news['headlines']).toarray()


prediction = model.predict(processed_features_new_data)
print(prediction)
lists = prediction.tolist()
my_json_string = json.dumps(lists)


for i in range(len(prediction)):
    if prediction[i] == 1:
        resultsPos.append(fresh_news['headlines'][i])
        overall += 1;
        print("Positive: " + fresh_news['headlines'][i])
    if prediction[i] == -1:
        resultsNeg.append(fresh_news['headlines'][i])
        overall -= 1;
        print("Negative: " + fresh_news['headlines'][i])
