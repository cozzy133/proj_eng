import csv
import pandas as pd
import nltk
import warnings

warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

# stock market lexicon
stock_lex = pd.read_csv('/root/PycharmProjects/proj_eng/sentiment analyser/effort2/lexicon_data')
stock_lex['sentiment'] = (stock_lex['Aff_Score'] + stock_lex['Neg_Score']) / 2
stock_lex = dict(zip(stock_lex.Item, stock_lex.sentiment))
stock_lex = {k: v for k, v in stock_lex.items() if len(k.split(' ')) == 1}
stock_lex_scaled = {}
for k, v in stock_lex.items():
    if v > 0:
        stock_lex_scaled[k] = v / max(stock_lex.values()) * 4
    else:
        stock_lex_scaled[k] = v / min(stock_lex.values()) * -4

# Loughran and McDonald
positive = []
with open('lexicon_data/lm_positive.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        positive.append(row[0].strip())

negative = []
with open('lexicon_data/lm_negative.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        entry = row[0].strip().split(" ")
        if len(entry) > 1:
            negative.extend(entry)
        else:
            negative.append(entry[0])

final_lex = {}
final_lex.update({word:2.0 for word in positive})
final_lex.update({word:-2.0 for word in negative})
final_lex.update(stock_lex_scaled)
final_lex.update(sia.lexicon)
sia.lexicon = final_lex
