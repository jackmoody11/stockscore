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
    # Get data for screen
    if dividends is None:
        dividends = utils.get_dividends(batch_data)
    for symbol in dividends:
        try:
            symbol_dividends = dividends[symbol]
            years = len(symbol_dividends) // 4
            pts = years
            stock_scores.loc[symbol][
                "Value Score"
            ] += pts  # Add numbers of years which dividends have been paid
        except (KeyError, IndexError):
            continue  # Skip to next stock if unable to get data

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
    # Get data for screen
    if financials is None:
        financials = utils.get_financials(batch_data)
    # Give score based on net income results from the past year
    for symbol in financials:
        try:
            symbol_financials = financials[symbol]["financials"]["financials"]
            quarters = len(symbol_financials)
            try:
                if all(symbol_financials[i]["netIncome"] > 0 for i in range(quarters)):
                    pts = quarters
                    stock_scores.loc[symbol][
                        "Value Score"
                    ] += pts  # positive net income for all quarters reporting
            except (KeyError, TypeError):
                continue
        except (KeyError, TypeError):
            continue  # Skip to next stock if unable to get data

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
    # Get data for screen
    if financials is None:
        financials = utils.get_financials(batch_data)
    # Give score based on current ratio (measure of ability to cover short term debt obligations
    for symbol, _ in stock_scores.iterrows():
        try:
            fin_base = financials[symbol]["financials"]["financials"][0]
            current_assets = fin_base["currentAssets"]
            current_debt = fin_base["currentDebt"]
            try:
                current_ratio = current_assets / current_debt
                if current_ratio >= 1.5:
                    stock_scores.loc[symbol]["Value Score"] += 2
                    # print(f"{symbol} score went up by 2 -- current ratio >= 1.5")
                elif current_ratio >= 1:
                    stock_scores.loc[symbol]["Value Score"] += 1
                    # print(f"{symbol} score went up by 1 -- current ratio >= 1")
            except ZeroDivisionError:
                if isinstance(current_assets, int or float) and current_assets > 0:
                    stock_scores.loc[symbol][
                        "Value Score"
                    ] += 1  # company has no short term obligations to pay
                continue  # If data is bad, skip to next stock
            except TypeError:
                if (
                    current_debt is None
                    and current_assets is not None
                    and current_assets > 0
                ):
                    stock_scores.loc[symbol][
                        "Value Score"
                    ] += 1  # company has no short term obligations to pay
                continue  # If data is bad, skip to next stock
        except (KeyError, TypeError):
            continue  # If current assets and current debt stats are not available, skip to next stock

    return stock_scores


def p_to_b_test(symbols, stock_scores, stats=None):
    """
    :param symbols: List of symbols
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Defaults as None, but can be set to value to speed up performance if running suite
    or multiple tests at once.
    :return: Returns updated stock_score dictionary. Make sure to set stock_score to the function
    so that p_to_b_test() returns updated stock scores.
    """
    # Get data for screen
    if stats is None:
        stats = utils.get_stats(symbols)
    # Give score based on price/book ratio - criteria taken from Ben Graham's Intelligent Investor
    for symbol, _ in stock_scores.iterrows():
        try:
            if 0 < stats.loc[symbol]["priceToBook"] <= 1.2:
                pts = 1
                stock_scores.loc[symbol]["Value Score"] += pts
                # print(f"{symbol} score went up by {pts}-- price to book between 0 and 1.2")
        except (TypeError, KeyError):
            continue  # If price/book ratio is not given, skip to next symbol

    return stock_scores


def pe_ratio_test(symbols, batch_data, stock_scores, chart=None, stats=None):
    # Get data for screen
    if stats is None:
        stats = utils.get_stats(symbols)
    if chart is None:
        chart = utils.get_chart(batch_data)
    # Give score based on price/earnings ratio
    for symbol, _ in stock_scores.iterrows():
        try:
            ttm_eps = stats.loc[symbol]["ttmEPS"]
            price = chart[symbol][0]["close"]
            pe_ratio = price / ttm_eps
            if 0 < pe_ratio <= 15:
                stock_scores.loc[symbol]["Value Score"] += 2
                # print(
                #     f"{symbol} score went up by 2 -- P/E ratio positive and less than 15"
                # )
            elif 15 < pe_ratio < 30:
                stock_scores.loc[symbol]["Value Score"] += 1
                # print(
                #     f"{symbol} score went up by 1 -- P/E ratio positive and between 15 and 30"
                # )
        except (ZeroDivisionError, IndexError, KeyError):
            continue  # if earnings is zero or EPS is not available, go to next symbol

    return stock_scores


def suite(
    symbols, batch_data, stock_scores, dividends=None, financials=None, stats=None
):

    """
    Runs all tests within fundamental_functions at once
    :param symbols: List of symbols
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
    stock_scores = p_to_b_test(symbols, stock_scores, stats=stats)
    stock_scores = pe_ratio_test(symbols, batch_data, stock_scores, stats=stats)
    return stock_scores
