from stockScore import start
from math import floor


# Needs updating
def dividend_test(batch_data, stock_scores, dividends=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param dividends: Dictionary with all dividend information from IEX API (see get_dividends in start
    module for more info.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that dividend_test() can return updated stock scores.
    """
    if dividends is None:
        dividends = start.get_dividends(batch_data)
    for symbol in dividends:
        try:
            symbol_dividends = dividends[symbol]['dividends']
            years = floor(len(symbol_dividends)/4)
            stock_scores[symbol] += years
            print(f'{symbol} score went up by {years} -- paid dividends for the \
                  last {years} years')
        except (KeyError, IndexError):
            continue

    return stock_scores


def net_income_test(batch_data, stock_scores, financials=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param financials: Dictionary with all financial information from IEX API (see get_financials in start
    module for more info.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that net_income_test() can return updated stock scores.
    """
    if financials is None:
        financials = start.get_financials(batch_data)
    for symbol in financials:
        try:
            symbol_financials = financials[symbol]['financials']['financials']
            years = len(symbol_financials)
            try:
                if all(symbol_financials[i]['netIncome'] > 0 for i in range(0, years)):
                    stock_scores[symbol] += years
                    print(f'{symbol} score went up by {years} -- positive net income for the \
                          last {years} years')
                elif symbol_financials[0]['netIncome'] and \
                        symbol_financials[0]['netIncome'] > 0:
                    stock_scores[symbol] += 1
                    print(f'{symbol} score went up by 1 -- positive net income last year')
            except (KeyError, TypeError):
                continue
        except (KeyError, TypeError):
            continue

    return stock_scores


def current_ratio_test(batch_data, stock_scores, financials=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param financials: Dictionary with all financial information from IEX API (see get_financials in start
    module for more info.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that current_ratio() can return updated stock scores.
    """
    if financials is None:
        financials = start.get_financials(batch_data)
    for symbol in stock_scores:
        try:
            current_assets = financials[symbol]['financials']['financials'][0]['currentAssets']
            current_debt = financials[symbol]['financials']['financials'][0]['currentDebt']
            try:
                current_ratio = current_assets/current_debt
                if current_ratio >= 1.5:
                    stock_scores[symbol] += 2
                    print(f'{symbol} score went up by 2 -- current ratio >= .5')
                elif current_ratio >= 1:
                    stock_scores[symbol] += 1
                    print(f'{symbol} score went up by 1 -- current ratio >= 1')
            except (ZeroDivisionError, TypeError):
                continue
        except (KeyError, TypeError):
            continue

    return stock_scores


def suite(batch_data, stock_scores, financials=None):

    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param financials: Dictionary with all financial information from IEX API (see get_financials in start
    module for more info.
    :return: Returns an updated stock_score dictionary that runs all functions
    in fundamental_functions module. Make sure to set stock_score to the function
    so that suite() can return updated stock scores.
    """
    stock_scores = dividend_test(batch_data, stock_scores)
    stock_scores = net_income_test(batch_data, stock_scores, financials)
    stock_scores = current_ratio_test(batch_data, stock_scores, financials)
    return stock_scores
