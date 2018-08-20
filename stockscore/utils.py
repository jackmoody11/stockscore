# Modules
from bs4 import BeautifulSoup
import grequests
import requests

iex_url_base = "https://api.iextrading.com/1.0/"


def get_symbols():
    """
    :return: Gets all symbols(tickers) from IEX API
    """
    symbols_json = requests.get(iex_url_base + "ref-data/symbols").json()
    symbols = [symbol["symbol"] for symbol in symbols_json if symbol["type"] == "cs"]
    return symbols


def init_stock_scores(symbols):
    """Set all stock scores to zero. """
    stock_scores = {symbol: 0 for symbol in symbols}
    return stock_scores


def set_batches(symbols):
    """
    :param symbols: Give list of stock symbols
    :return: Concatenates stock symbols in lumps of
    up to 100 to allow for batch GET requests from IEX API
    """
    batches = [",".join(symbols[i : i + 100]) for i in range(0, len(symbols), 100)]
    return batches


def get_responses(payloads):

    """
    :param payloads: list of payloads for GET request
    :return: Returns all batch GET requests from API for given url_end.
    """
    batch_url = f"{iex_url_base}stock/market/batch?"
    rs = (grequests.get(batch_url, params=payload) for payload in payloads)
    result = grequests.map(rs)
    outputs = [r.json() for r in result]
    return outputs


def get_stats(batch_data):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :return: Gives dictionary of each symbol's statistics. To get individual
    statistic for individual stock, use something of the general form stats[symbol]['stats'][specific_stat].
    Note that 'stats' is fixed string.
    """
    payloads = [{"symbols": batch, "types": "stats"} for batch in batch_data]
    outputs = get_responses(payloads=payloads)
    stats = {
        symbol: outputs[outputs.index(batch_dict)][symbol]
        for batch_dict in outputs
        for symbol in batch_dict
    }
    return stats


def get_company(batch_data):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :return: Gives dictionary with each symbols info (sector, industry, CEO name, etc.)
    """
    payloads = [{"symbols": batch, "types": "company"} for batch in batch_data]
    outputs = get_responses(payloads=payloads)
    company = {
        symbol: outputs[outputs.index(batch_dict)][symbol]["company"]
        for batch_dict in outputs
        for symbol in batch_dict
    }
    return company


def get_chart(batch_data, time="1m"):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param time: Length of time (1m = 1 month, 1y = 1 year, etc.) can go up to 5y
    :return: Gives large list of statistics for symbols in batch_data. To get individual
    statistic for individual stock, use something of the general form stats[symbol]['stats'][specific_stat].
    Note that 'stats' is fixed string.
    """
    payloads = [
        {"symbols": batch, "types": "chart", "range": time} for batch in batch_data
    ]
    outputs = get_responses(payloads=payloads)
    chart = {
        symbol: outputs[outputs.index(batch_dict)][symbol]
        for batch_dict in outputs
        for symbol in batch_dict
    }
    return chart


def get_financials(batch_data):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :return: Gives large list of statistics for symbols in batch_data. To get individual
    statistic for individual stock, use something of the general form stats[symbol]['stats'][specific_stat].
    Note that 'stats' is fixed string.
    """
    payloads = [{"symbols": batch, "types": "financials"} for batch in batch_data]
    outputs = get_responses(payloads=payloads)
    financials = {
        symbol: outputs[outputs.index(batch_dict)][symbol]
        for batch_dict in outputs
        for symbol in batch_dict
    }
    return financials


def get_splits(batch_data, time="1y"):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param time: Length of time (1m = 1 month, 1y = 1 year, etc.) can go up to 5y
    :return: Dictionary of stock splits
    """
    payloads = [
        {"symbols": batch, "types": "splits", "range": time} for batch in batch_data
    ]
    outputs = get_responses(payloads=payloads)
    splits = {
        symbol: outputs[outputs.index(batch_dict)][symbol]
        for batch_dict in outputs
        for symbol in batch_dict
    }
    return splits


def get_dividends(batch_data, time="5y"):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param time: Length of time (1m = 1 month, 1y = 1 year, etc.) can go up to 5y
    :return: Dictionary of stock dividends
    """
    payloads = [
        {"symbols": batch, "types": "dividends", "range": time} for batch in batch_data
    ]
    outputs = get_responses(payloads=payloads)
    dividends = {
        symbol: outputs[outputs.index(batch_dict)][symbol]
        for batch_dict in outputs
        for symbol in batch_dict
    }
    return dividends


def total_setup():
    """
    :return: Total setup returns symbols, stock_scores, and batch_symbols.
    """
    symbols = get_symbols()
    stock_scores, batch_symbols = init_stock_scores(symbols), set_batches(symbols)
    return symbols, stock_scores, batch_symbols


def soup_it(url):
    """
    :param url: Give url for HTML code to be copied
    :return: Returns parsed HTML code (to strip info from)
    """
    page = requests.get(url).text.encode("utf-8").decode("ascii", "ignore")
    soup = BeautifulSoup(page, "html.parser")
    return soup


def return_top(dictionary, x=None):
    """
    :param dictionary: Give a dictionary with numeric values (ex: {'Ticker1':200, 'Ticker2':300, 'Ticker3':450})
    :param x: # of keys to be returned. Function defaults to return entire dictionary sorted.
    :return: Will return top x values with keys.
    """
    x = len(dictionary) if x is None else x
    sorted_array = sorted(dictionary.items(), key=lambda a: a[1], reverse=True)
    return sorted_array[0:x]
