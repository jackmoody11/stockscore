from stockscore import utils


# Needs updating
def dividend_test(batch_data, stock_scores, dividends=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param dividends: Dictionary with all dividend information from IEX API (see get_dividends in utils
    module for more info.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that dividend_test() can return updated stock scores.
    """
    if dividends is None:
        dividends = utils.get_dividends(batch_data)
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
    :param financials: Dictionary with all financial information from IEX API (see get_financials in utils
    module for more info.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that net_income_test() can return updated stock scores.
    """
    if financials is None:
        financials = utils.get_financials(batch_data)
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
    :param financials: Dictionary with all financial information from IEX API (see get_financials in utils
    module for more info.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that current_ratio() can return updated stock scores.
    """
    if financials is None:
        financials = utils.get_financials(batch_data)
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


def p_to_b_test(batch_data, stock_scores, stats=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Defaults as None, but can be set to value to speed up performance if running suite
    or multiple tests at once.
    :return: Returns updated stock_score dictionary. Make sure to set stock_score to the function
    so that p_to_b_test() returns updated stock scores.
    """
    if stats is None:
        stats = utils.get_stats(batch_data)

    for symbol in stock_scores:
        try:
            if 0 < stats[symbol]["stats"]["priceToBook"] <= 1.2:
                pts = 1
                stock_scores[symbol] += pts
                # print(f"{symbol} score went up by {pts}-- price to book between 0 and 1.2")
        except (TypeError, KeyError):
            continue

    return stock_scores


def pe_ratio_test(batch_data, stock_scores, chart=None, stats=None):

    if stats is None:
        stats = utils.get_stats(batch_data)
    if chart is None:
        chart = utils.get_chart(batch_data)
    for symbol in stock_scores:
        try:
            ttm_eps = stats[symbol]["stats"]["ttmEPS"]
            price = chart[symbol]["chart"][0]["close"]
            pe_ratio = price / ttm_eps
            if 0 < pe_ratio <= 15:
                stock_scores[symbol] += 2
                # print(
                #     f"{symbol} score went up by 2 -- P/E ratio positive and less than 15"
                # )
            elif 15 < pe_ratio < 30:
                stock_scores[symbol] += 1
                # print(
                #     f"{symbol} score went up by 1 -- P/E ratio positive and between 15 and 30"
                # )
        except (ZeroDivisionError, IndexError, KeyError):
            continue

    return stock_scores


def suite(batch_data, stock_scores, dividends=None, financials=None, stats=None):

    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param dividends: Dictionary with all dividend information from IEX API (see get_dividends in utils
    module for more info.
    :param financials: Dictionary with all financial information from IEX API (see get_financials in utils
    module for more info.
    :param stats: Dictionary with all stats information from IEX API (see get_stats in utils
    module for more info.
    :return: Returns an updated stock_score dictionary that runs all functions
    in fundamental_functions module. Make sure to set stock_score to the function
    so that suite() can return updated stock scores.
    """
    stock_scores = dividend_test(batch_data, stock_scores, dividends=dividends)
    stock_scores = net_income_test(batch_data, stock_scores, financials=financials)
    stock_scores = current_ratio_test(batch_data, stock_scores, financials=financials)
    stock_scores = p_to_b_test(batch_data, stock_scores, stats=stats)
    stock_scores = pe_ratio_test(batch_data, stock_scores, stats=stats)
    return stock_scores
