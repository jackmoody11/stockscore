from bs4 import BeautifulSoup
import requests


iex_url_base = "https://api.iextrading.com/1.0/"

def get_symbols(iex_url_base):

	symbols_json = requests.get(iex_url_base + "ref-data/symbols").json()
	symbols = []
	for i in range(len(symbols_json)):
	    if symbols_json[i]['type'] == 'cs':
	        symbols.append(symbols_json[i]['symbol'])
	return symbols


def init_stock_scores(symbols):

	stock_scores = {}
	for symbol in symbols:
	    stock_scores[symbol] = 0
	return stock_scores


# Calculate number of batches to GET
def set_batches(symbols):

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


def soup_it(url):

    page = requests.get(url).text.encode("utf-8").decode('ascii', 'ignore')
    soup = BeautifulSoup(page, 'html.parser')
    return soup