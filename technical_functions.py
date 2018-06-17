import requests
iex_url_base = "https://api.iextrading.com/1.0/"


def suite(batch_symbols, stock_scores, api_url_base = iex_url_base):

    stock_scores = moving_avg_test(batch_symbols, stock_scores)
    return stock_scores

def moving_avg_test(batch_symbols, stock_scores, api_url_base = iex_url_base):

    for i in batch_symbols:
        batch_url = api_url_base + "stock/market/batch?symbols=" + batch_symbols[i] + "&types=stats"
        result = requests.get(batch_url).json()
        for symbol in result:
            base = result[symbol]['stats']
            if(base['day200MovingAvg'] and base['day50MovingAvg']):
                avg_50 = base['day50MovingAvg']
                avg_200 = base['day200MovingAvg']
                per_diff = ((avg_50 - avg_200)/avg_200) * 100
                score = per_diff
                if(0 < per_diff < 2):
                    stock_scores[symbol] += round(5/(score + 1))
                    print(symbol + " score went up by " + str(round(5/(score+1))) + " -- SMA 200 under SMA 50 by " + str(per_diff) + "%")
                elif(2 < per_diff < 5):
                    stock_scores[symbol] += round(5/score)
                    print(symbol + " score went up by " + str(round(5/score)) + " -- SMA 200 under SMA 50 by " + str(per_diff) + "%")
    return stock_scores
