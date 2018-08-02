# Modules
from bs4 import BeautifulSoup
import requests
import multiprocessing
import os
from math import ceil

iex_url_base = "https://api.iextrading.com/1.0/"


def get_symbols():
    """
    :return: Gets all symbols(tickers) from IEX API
    """
    symbols_json = requests.get(iex_url_base + "ref-data/symbols").json()
    symbols = []
    for i in range(len(symbols_json)):
        if symbols_json[i]["type"] == "cs":
            symbols.append(symbols_json[i]["symbol"])
    return symbols


def init_stock_scores(symbols):
    """Set all stock scores to zero. """
    stock_scores = {}
    for symbol in symbols:
        stock_scores[symbol] = 0
    return stock_scores


def set_batches(symbols):
    """
    :param symbols: Give list of stock symbols
    :return: Concatenates stock symbols in lumps of
    up to 100 to allow for batch GET requests from IEX API
    """
    num_batches = int(ceil(len(symbols) / 100))
    x = 0
    batch_symbols = []
    for i in range(0, num_batches):
        if x + 99 <= len(symbols):
            batch_symbols.append(",".join(symbols[x: x + 99]))
        else:
            batch_symbols.append(",".join(symbols[x: len(symbols) + 1]))
            break
        x = (i + 1) * 100
    return batch_symbols


def split_symbols(symbols, n=100):
    # Don't use this until PR is accepted for iexfinance module
    sym_list = list()
    for i in range(0, len(symbols), n):
        sym_list.append(symbols[i:i+n])
    return sym_list


def batch_get(batch, url_end):
    """
    Note: This function is only intended to be used for get_pool_response() function in start module,
    but SHOULD NOT be embedded into get_pool_response to avoid pickling problems.
    :param batch: Give a single batch of tickers (ex: 'A,AA,AAPL,...,MSFT')
    :param url_end: Add the query that you will be using  (ex: "&types=dividends&range=5y")
    :return: all the data necessary to make multiple get requests at once
    """
    batch_url = f"{iex_url_base}stock/market/batch?symbols={batch}{url_end}"
    response = requests.get(batch_url).json()
    return response


def get_pool_response(batch_data, url_end, num_processes=os.cpu_count()):

    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param url_end: Add the query that you will be using  (ex: "&types=dividends&range=5y")
    :param num_processes: Defaults to # of computer cores, but it is possible to have more.
    Increase this as your computer capacity allows for faster multiprocessing.
    :return: Returns all batch GET requests from API for given url_end.
    """
    pool = multiprocessing.Pool(processes=num_processes)
    outputs = []
    outputs.append(pool.starmap(batch_get, [[batch, url_end] for batch in batch_data]))
    pool.close()
    pool.join()
    return outputs


def get_stats(batch_data):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :return: Gives large list of statistics for symbols in batch_data. To get individual
    statistic for individual stock, use something of the general form stats[symbol]['stats'][specific_stat].
    Note that 'stats' is fixed string.
    """
    stats = {}
    outputs = get_pool_response(batch_data, "&types=stats")[0]
    for batch_dict in outputs:
        for symbol in batch_dict:
            batch_index = outputs.index(batch_dict)
            stats[symbol] = outputs[batch_index][symbol]
    return stats


def get_chart(batch_data, time="1m"):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param time: Length of time (1m = 1 month, 1y = 1 year, etc.) can go up to 5y
    :return: Gives large list of statistics for symbols in batch_data. To get individual
    statistic for individual stock, use something of the general form stats[symbol]['stats'][specific_stat].
    Note that 'stats' is fixed string.
    """
    chart = {}
    outputs = get_pool_response(batch_data, f"&types=chart&range={time}")[0]
    for batch_dict in outputs:
        for symbol in batch_dict:
            batch_index = outputs.index(batch_dict)
            chart[symbol] = outputs[batch_index][symbol]
    return chart


def get_financials(batch_data):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :return: Gives large list of statistics for symbols in batch_data. To get individual
    statistic for individual stock, use something of the general form stats[symbol]['stats'][specific_stat].
    Note that 'stats' is fixed string.
    """
    financials = {}
    outputs = get_pool_response(batch_data, "&types=financials")[0]
    for batch_dict in outputs:
        for symbol in batch_dict:
            batch_index = outputs.index(batch_dict)
            financials[symbol] = outputs[batch_index][symbol]
    return financials


def get_splits(batch_data, time="1y"):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param time: Length of time (1m = 1 month, 1y = 1 year, etc.) can go up to 5y
    :return: Dictionary of stock splits
    """
    splits = {}
    outputs = get_pool_response(batch_data, f"&types=splits&range={time}")[0]
    for batch_dict in outputs:
        for symbol in batch_dict:
            batch_index = outputs.index(batch_dict)
            splits[symbol] = outputs[batch_index][symbol]
    return splits


def get_dividends(batch_data, time="5y"):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param time: Length of time (1m = 1 month, 1y = 1 year, etc.) can go up to 5y
    :return: Dictionary of stock dividends
    """
    dividends = {}
    outputs = get_pool_response(batch_data, f"&types=dividends&range={time}")[0]
    for batch_dict in outputs:
        for symbol in batch_dict:
            batch_index = outputs.index(batch_dict)
            dividends[symbol] = outputs[batch_index][symbol]
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
    if x is None:
        x = len(dictionary)
    sorted_array = sorted(dictionary.items(), key=lambda a: a[1], reverse=True)
    return sorted_array[0:x]
