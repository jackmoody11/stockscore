from stockScore import start


def net_income_test(batch_data, stock_scores):

    """Adds 1 point to all stocks that have paid dividends the past four years.

    Must already have stock_scores dictionary. To add this test, run stock_scores = ff.dividend_test(...)."""
    # Get data through multiprocessing
    pool_outputs = start.get_pool_response(batch_data, "&types=financials&range=5y")
    for first in pool_outputs:
        for batch in first:
            for ni_json in batch:
                for symbol in ni_json:
                    if ni_json[symbol]['financials']['financials'] is not None:
                        base = ni_json[symbol]['financials']['financials']
                        base_length = len(base)
                        if all(base[i]['netIncome'].is_numeric() for i in range(0, base_length)) \
                                and all(base[j]['netIncome'] > 0 for j in range(0, base_length)):
                            stock_scores[symbol] += base_length
                            print(symbol + " score went up by " + str(
                                base_length) + " -- positive net income for the last " + str(base_length) + " years")
                        elif base[0]['netIncome'].is_numeric() and base[0]['netIncome'] > 0:
                            stock_scores[symbol] += 1
                            print(symbol + " score went up by 1 -- positive net income last year")

    return stock_scores


symbols = start.get_symbols()
batches = start.set_batches(symbols)
stock_scores = start.init_stock_scores(symbols)
stock_scores = net_income_test(batches, stock_scores)
print(stock_scores)
