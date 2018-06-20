from bs4 import BeautifulSoup
import requests

iex_url_base = "https://api.iextrading.com/1.0/"


def get_symbols(iex_url_base):

	"""Gets all symbols from IEX API (uppercase). """
	symbols_json = requests.get(iex_url_base + "ref-data/symbols").json()
	symbols = []
	for i in range(len(symbols_json)):
	    if symbols_json[i]['type'] == 'cs':
	        symbols.append(symbols_json[i]['symbol'])
	return symbols


def init_stock_scores(symbols):

	"""Set all stock scores to zero. """
	stock_scores = {}
	for symbol in symbols:
	    stock_scores[symbol] = 0
	return stock_scores


def set_batches(symbols):

	"""Calculate number of batches to send for GET request.

	Creates batches of 100 tickers to limit number of GET requests sent to IEX.
	"""
	num_batches = int(len(symbols) / 100 + round(len(symbols) % 100))
	x = 0
	batch_symbols = {}
	for i in range(0, num_batches):
	    if(x + 101 < len(symbols)):
	        batch_symbols[i] = ",".join(symbols[x:x + 100])
	    else:
	        batch_symbols[i] = ",".join(symbols[x:len(symbols) + 1])
	        break
	    x = (i + 1) * 100 + 1
	return batch_symbols


def total_setup(api_url_base = iex_url_base):

	symbols = get_symbols(api_url_base)
	stock_scores = init_stock_scores(symbols)
	batch_symbols = set_batches(symbols)
	return symbols, stock_scores, batch_symbols


def soup_it(url):

	"""Returns html from specified url using Beautiful Soup.

	Must further strip to meaningfully use the returned html result.
	"""
	page = requests.get(url).text.encode("utf-8").decode('ascii', 'ignore')
	soup = BeautifulSoup(page, 'html.parser')
	return soup



def return_top(dict, x = None):

	if x == None:
		x = len(dict)
	sorted_array = sorted(dict.items(), key=lambda x: x[1], reverse = True)
	return sorted_array[0:x]

