# Stock Score script created by Jack Moody 2018
#
# For each stock test, expect to spend about 20 seconds per test used
#
# Other useful libraries that can be used:
# import time
# import numpy as np

from bs4 import BeautifulSoup

import requests
# import matplotlib.pyplot as plt


iex_url_base = "https://api.iextrading.com/1.0/"


def soupit(url):

    page = requests.get(url).text.encode("utf-8").decode('ascii', 'ignore')
    soup = BeautifulSoup(page, 'html.parser')
    return soup

symbols_json = requests.get(iex_url_base + "ref-data/symbols").json()
symbols = []
for i in range(len(symbols_json)):
    if symbols_json[i]['type'] == 'cs':
        symbols.append(symbols_json[i]['symbol'].lower())

stock_scores = {}
for symbol in symbols:
    stock_scores[symbol] = 0

# Calculate number of batches to GET
num_batches = int(len(symbols) / 100 + round(len(symbols) % 100))
# Set batch strings for GET requests
x = 0
batch_symbols = {}

for i in range(0, num_batches):
    if(x + 101 < len(symbols)):
        batch_symbols[i] = ",".join(symbols[x:x + 100])
    else:
        batch_symbols[i] = ",".join(symbols[x:len(symbols) + 1])
        break
    x = (i + 1) * 100 + 1


def dividend_test(batch_tickers, api_url_base, scores):
    for i in batch_tickers:
        div_batch_url = api_url_base + "stock/market/batch?symbols=" + batch_tickers[i] + "&types=dividends&range=5y"
        div_json = requests.get(div_batch_url).json()
        for symbol in div_json:
            if(div_json[symbol.upper()].get('dividends') and len(div_json[symbol.upper()]['dividends']) >= 16):
                scores[symbol.lower()] += 1
                print(symbol + " score went up by 1 -- good dividends")
    return scores


def net_income_test(batch_symbols, iex_url_base, stock_scores):
    for i in batch_symbols:
        batch_url = iex_url_base + "stock/market/batch?symbols=" + batch_symbols[i] + "&types=financials&range=5y"
        result = requests.get(batch_url).json()
        for symbol in result:
        	if(result[symbol.upper()].get('financials')):
        		base = result[symbol]['financials']['financials']
        		base_length = len(base)
        		if(all(base[i]['netIncome'] for i in range(0, base_length))):
        			stock_scores[symbol.lower()] += base_length
        			print(symbol + " score went up by " + str(base_length) + " -- positive net income for the last " + str(base_length) + " years")
        		elif(base[0]['netIncome']):
        			stock_scores[symbol.lower()] += 1
        			print(symbol + " score went up by 1 -- positive net income last year")
    return stock_scores


def p_to_b_test(batch_symbols, iex_url_base, stock_scores):
    for i in batch_symbols:
        batch_url = iex_url_base + "stock/market/batch?symbols=" + batch_symbols[i] + "&types=stats"
        result = requests.get(batch_url).json()
        for symbol in result:
            if(result[symbol.upper()].get('stats')):
                base = result[symbol]['stats']
                # Price to book test -- Want a lower price to book
                if(base['priceToBook']):
                    score = round(5 / (base['priceToBook'] + 0.8))
                    if(0 < base['priceToBook'] <= 1):
                        stock_scores[symbol.lower()] += score
                        print(symbol + " score went up by " + str(score) + "-- price to book between 0 and 1")
                    elif(1 < base['priceToBook'] <= 2):
                        stock_scores[symbol.lower()] += score
                        print(symbol + " score went up by " + str(score) + "-- price to book between 1 and 2")
    return stock_scores


def moving_avg_test(batch_symbols, iex_url_base, stock_scores):
    for i in batch_symbols:
        batch_url = iex_url_base + "stock/market/batch?symbols=" + batch_symbols[i] + "&types=stats"
        result = requests.get(batch_url).json()
        for symbol in result:
            base = result[symbol]['stats']
            if(base['day200MovingAvg'] and base['day50MovingAvg']):
                avg_50 = base['day50MovingAvg']
                avg_200 = base['day200MovingAvg']
                per_diff = ((avg_50 - avg_200)/avg_200) * 100
                score = per_diff
                if(0 < per_diff < 2):
                    stock_scores[symbol.lower()] += round(5/(score + 1))
                    print(symbol + " score went up by " + str(round(5/(score+1))) + " -- SMA 200 under SMA 50 by " + str(per_diff) + "%")
                elif(2 < per_diff < 5):
                    stock_scores[symbol.lower()] += round(5/score)
                    print(symbol + " score went up by " + str(round(5/score)) + " -- SMA 200 under SMA 50 by " + str(per_diff) + "%")
    return stock_scores

stock_scores = net_income_test(batch_symbols, iex_url_base, stock_scores)
stock_scores = dividend_test(batch_symbols, iex_url_base, stock_scores)
stock_scores = p_to_b_test(batch_symbols, iex_url_base, stock_scores)
stock_scores = moving_avg_test(batch_symbols, iex_url_base, stock_scores)
print(stock_scores)


