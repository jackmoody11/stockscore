import requests
iex_url_base = "https://api.iextrading.com/1.0/"


def suite(batch_symbols, stock_scores, api_url_base = iex_url_base):

	stock_scores = p_to_b_test(batch_symbols, stock_scores)
	return stock_scores


def p_to_b_test(batch_symbols, stock_scores, api_url_base = iex_url_base):

	for i in batch_symbols:
		batch_url = api_url_base + "stock/market/batch?symbols=" + batch_symbols[i] + "&types=stats"
		result = requests.get(batch_url).json()
		for symbol in result:
			if(result[symbol.upper()].get('stats')):
				base = result[symbol]['stats']
				# Price to book test -- Want a lower price to book
				if(base['priceToBook']):
					score = round(5 / (base['priceToBook'] + 0.8))
					if(0 < base['priceToBook'] <= 1):
						stock_scores[symbol] += score
						print(symbol + " score went up by " + str(score) + "-- price to book between 0 and 1")
					elif(1 < base['priceToBook'] <= 2):
						stock_scores[symbol] += score
						print(symbol + " score went up by " + str(score) + "-- price to book between 1 and 2")

	return stock_scores

def get_stats(batch_symbols, api_url_base = iex_url_base):
	stock_stats = {}

	for i in range(len(batch_symbols)):
		batch_url = api_url_base + "stock/market/batch?symbols=" + batch_symbols[i] + "&types=stats"
		result = requests.get(batch_url).json()
		for symbol in result:
			if(result[symbol.upper()].get('stats')):
				stock_stats[symbol] = result[symbol]['stats']

	return stock_stats


print(get_stats(['AAPL', 'MSFT', 'AMD']))
