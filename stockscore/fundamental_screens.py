from stockscore import utils


# Needs updating
def dividend_test(batch_data, stock_scores, dividends=None):
    """
    :param batch_data: List of concatenated symbol batches
    :type batch_data: list
    :param stock_scores: Pandas DataFrame with stock scores
    :type stock_scores: Pandas DataFrame
    :param dividends: Dictionary with all dividend information from IEX API
    :type dividends: dict
    :return: Updated stock_scores Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    dividends = (
        utils.get_dividends(batch_data) if dividends is None else dividends
    )  # Get data for screen
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
    :param batch_data: List of concatenated symbols
    :type batch_data: list
    :param stock_scores: Pandas DataFrame with stock scores
    :type stock_scores: Pandas DataFrame
    :param financials: Dictionary with all financial information from IEX API
    :type financials: dict
    :return: Updated stock_scores Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    # Get data for screen
    financials = utils.get_financials(batch_data) if financials is None else financials
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
    :param batch_data: List of concatenated symbols
    :type batch_data: list
    :param stock_scores: Pandas DataFrame with stock scores
    :type stock_scores: Pandas DataFrame
    :param financials: Dictionary with all financial information from IEX API
    :type financials: dict
    :return: Updated stock_scores Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    # Get data for screen
    financials = utils.get_financials(batch_data) if financials is None else financials
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
    :type symbols: list
    :param stock_scores: Pandas DataFrame with stock scores
    :type stock_scores: Pandas DataFrame
    :param stats: Pandas DataFrame with all key stats from IEX API
    :type stats: Pandas DataFrame
    :return: Updated stock_scores Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    # Get data for screen
    stats = utils.get_stats(symbols) if stats is None else stats
    # Give score based on price/book ratio - criteria taken from Ben Graham's Intelligent Investor
    for symbol, _ in stock_scores.iterrows():
        try:
            pts = 1
            stock_scores.loc[symbol]["Value Score"] += (
                pts if 0 < stats.loc[symbol]["priceToBook"] <= 1.2 else 0
            )
        except TypeError:
            continue  # If price/book ratio is not given, skip to next symbol

    return stock_scores


def pe_ratio_test(symbols, stock_scores, close=None, stats=None):
    """
    :param symbols: List of symbols
    :type symbols: list
    :param stock_scores: Pandas DataFrame with stock scores
    :type stock_scores: Pandas DataFrame
    :param close: Pandas DataFrame with closing prices of symbols
    :type close: Pandas DataFrame
    :param stats: Pandas DataFrame with all key stats provided by IEX API
    :type stats: Pandas DataFrame
    :return: Updated stock_scores Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    # Get data for screen
    stats = utils.get_stats(symbols) if stats is None else stats
    close = utils.get_close(symbols) if close is None else close
    # Give score based on price/earnings ratio
    for symbol, _ in stock_scores.iterrows():
        try:
            ttm_eps = stats.loc[symbol]["ttmEPS"]
            price = close.loc[symbol]["close"]
            pe_ratio = price / ttm_eps
            if 0 < pe_ratio <= 15:
                stock_scores.loc[symbol]["Value Score"] += 2
            elif 15 < pe_ratio < 30:
                stock_scores.loc[symbol]["Value Score"] += 1
        except (ZeroDivisionError, TypeError):
            continue  # if earnings is zero or EPS is not available, go to next symbol

    return stock_scores


def suite(
    symbols,
    batch_data,
    stock_scores,
    dividends=None,
    financials=None,
    stats=None,
    close=None,
):

    """
    Runs all tests within fundamental_functions at once
    :param symbols: List of symbols
    :type symbols: list
    :param batch_data: List of concatenated symbols
    :type batch_data: list
    :param stock_scores: Pandas DataFrame with stock scores
    :type stock_scores: Pandas DataFrame
    :param dividends: Dictionary with all dividend information from IEX API
    :type dividends: dict
    :param financials: Dictionary with all financial information from IEX API
    :type financials: dict
    :param stats: Pandas DataFrame with all key stats from IEX API\
    :type stats: Pandas DataFrame
    :param close: Pandas DataFrame of all closing prices
    :type close: Pandas DataFrame
    :return: Updated stock_scores Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    stock_scores = dividend_test(batch_data, stock_scores, dividends=dividends)
    stock_scores = net_income_test(batch_data, stock_scores, financials=financials)
    stock_scores = current_ratio_test(batch_data, stock_scores, financials=financials)
    stock_scores = p_to_b_test(symbols, stock_scores, stats=stats)
    stock_scores = pe_ratio_test(symbols, stock_scores, stats=stats, close=close)
    return stock_scores
