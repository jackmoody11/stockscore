import requests
iex_url_base = "https://api.iextrading.com/1.0/"

def suite(batch_symbols, stock_scores, api_url_base = iex_url_base):

    stock_scores = dividend_test(batch_symbols, stock_scores)
    stock_scores = net_income_test(batch_symbols, stock_scores)
    return stock_scores


def dividend_test(batch_symbols, stock_scores, api_url_base = iex_url_base):

    """Adds 1 point to all stocks that have paid dividends the past four years.

    Must already have stock_scores dictionary. To add this test, run stock_scores += ff.dividend_test(...)."""
    for i in batch_symbols:
        div_batch_url = api_url_base + "stock/market/batch?symbols=" + batch_symbols[i] + "&types=dividends&range=5y"
        div_json = requests.get(div_batch_url).json()
        for symbol in div_json:
            if(div_json[symbol.upper()].get('dividends') and len(div_json[symbol.upper()]['dividends']) >= 16):
                stock_scores[symbol] += 1
                print(symbol + " score went up by 1 -- good dividends")
    return stock_scores


def net_income_test(batch_symbols, stock_scores, api_url_base = iex_url_base):

    for i in batch_symbols:
        batch_url = api_url_base + "stock/market/batch?symbols=" + batch_symbols[i] + "&types=financials&range=5y"
        result = requests.get(batch_url).json()
        for symbol in result:
        	if(result[symbol.upper()].get('financials')):
        		base = result[symbol]['financials']['financials']
        		base_length = len(base)
        		if(all(base[i]['netIncome'] for i in range(0, base_length))):
        			stock_scores[symbol] += base_length
        			print(symbol + " score went up by " + str(base_length) + " -- positive net income for the last " + str(base_length) + " years")
        		elif(base[0]['netIncome']):
        			stock_scores[symbol] += 1
        			print(symbol + " score went up by 1 -- positive net income last year")
    return stock_scores


