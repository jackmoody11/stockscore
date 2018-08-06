from stockScore import start


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
            symbol_dividends = dividends[symbol]["dividends"]
            years = len(symbol_dividends) // 4
            pts = years
            stock_scores[symbol] += pts
            # print(
            #     f"{symbol} score went up by {pts} -- paid dividends for the \
            #       last {years} years"
            # )
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
            symbol_financials = financials[symbol]["financials"]["financials"]
            quarters = len(symbol_financials)
            try:
                if all(symbol_financials[i]["netIncome"] > 0 for i in range(quarters)):
                    pts = 3
                    stock_scores[symbol] += pts
                    # print(
                    #     f"{symbol} score went up by {pts} -- positive net income for all quarters reporting"
                    # )

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
            fin_base = financials[symbol]["financials"]["financials"][0]
            current_assets = fin_base["currentAssets"]
            current_debt = fin_base["currentDebt"]
            try:
                current_ratio = current_assets / current_debt
                if current_ratio >= 1.5:
                    stock_scores[symbol] += 2
                    # print(f"{symbol} score went up by 2 -- current ratio >= .5")
                elif current_ratio >= 1:
                    stock_scores[symbol] += 1
                    # print(f"{symbol} score went up by 1 -- current ratio >= 1")
            except (ZeroDivisionError, TypeError):
                continue
        except (KeyError, TypeError):
            continue

    return stock_scores


def suite(batch_data, stock_scores, dividends=None, financials=None):

    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param dividends: Dictionary with all dividend information from IEX API (see get_dividends in start
    module for more info.
    :param financials: Dictionary with all financial information from IEX API (see get_financials in start
    module for more info.
    :return: Returns an updated stock_score dictionary that runs all functions
    in fundamental_functions module. Make sure to set stock_score to the function
    so that suite() can return updated stock scores.
    """
    stock_scores = dividend_test(batch_data, stock_scores, dividends=dividends)
    stock_scores = net_income_test(batch_data, stock_scores, financials=financials)
    stock_scores = current_ratio_test(batch_data, stock_scores, financials=financials)
    return stock_scores
