from stockScore import start
iex_url_base = "https://api.iextrading.com/1.0/"


def dividend_test(batch_data, stock_scores):

    """Adds 1 point to all stocks that have paid dividends the past four years.

    Must already have stock_scores dictionary. To add this test, run stock_scores = ff.dividend_test(...).
    (Assuming fundamental_functions is imported as ff)"""
    # Get data through multiprocessing
    pool_outputs = start.get_pool_response(batch_data, "&types=dividends&range=5y")

    for first in pool_outputs:
        for batch in first:
            for div_json in batch:
                for symbol in div_json:
                    if div_json[symbol].get('dividends'):
                        stock_scores[symbol] += 1

    return stock_scores


def net_income_test(batch_data, stock_scores):

    """Adds 1 point to all stocks that have paid dividends the past four years.

    Must already have stock_scores dictionary. To add this test, run stock_scores = ff.dividend_test(...)."""
    # Get data through multiprocessing
    pool_outputs = start.get_pool_response(batch_data, "&types=financials&range=5y")
    for first in pool_outputs:
        for batch in first:
            for ni_json in batch:
                for symbol in ni_json:
                    if ni_json[symbol].get('financials').get('financials') is not None:
                        base = ni_json[symbol]['financials']['financials']
                        base_length = len(base)
                        if all(base[i]['netIncome'] for i in range(0, base_length)) \
                                and all(base[j]['netIncome'] > 0 for j in range(0, base_length)):
                            stock_scores[symbol] += base_length
                            print(symbol + " score went up by " + str(
                                base_length) + " -- positive net income for the last " + str(base_length) + " years")
                        elif base[0]['netIncome'] and base[0]['netIncome'] > 0:
                            stock_scores[symbol] += 1
                            print(symbol + " score went up by 1 -- positive net income last year")

    return stock_scores


def suite(batch_symbols, stock_scores):

    stock_scores = dividend_test(batch_symbols, stock_scores)
    stock_scores = net_income_test(batch_symbols, stock_scores)
    return stock_scores
