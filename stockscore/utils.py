# Modules
from bs4 import BeautifulSoup
import grequests
import requests
import pandas as pd
import numpy as np
from iexfinance import Stock
from multiprocessing import Pool

iex_url_base = "https://api.iextrading.com/1.0/"


def get_symbols():
    """
    :return: Gets all symbols(tickers) from IEX API
    :rtype: list
    """
    symbols_json = requests.get(iex_url_base + "ref-data/symbols").json()
    symbols = [symbol["symbol"] for symbol in symbols_json if symbol["type"] == "cs"]
    return symbols


def split_symbols(symbols):
    """
    :param symbols: List of stock symbols (tickers)
    :type symbols: list
    :return: List of lists of symbols broken into sizes of 100 (until remainder is less than 100)
    :rtype: list
    """
    return [symbols[i : i + 99] for i in range(0, len(symbols), 99)]


def init_stock_scores(symbols):
    """Set all stock scores to zero.
    :param symbols: List of stock symbols (tickers)
    :type symbols: list
    :return: Dictionary of all stock_scores set to 0
    :rtype: dict
    """
    columns = ["Score", "Value Score", "Growth Score", "Momentum Score"]
    stock_scores = pd.DataFrame(
        np.zeros((len(symbols), len(columns))), index=symbols, columns=columns
    )
    return stock_scores


def set_batches(symbols):
    """
    :param symbols: List of stock symbols
    :type symbols: list
    :return: List of strings with 100 comma separated symbols (until remainder is less than 100)
    :rtype: list
    """
    batches = [",".join(symbols[i : i + 100]) for i in range(0, len(symbols), 100)]
    return batches


def get_responses(payloads):
    """
    :param payloads: List of payloads for GET request
    :type payloads: list
    :return: List of dictionaries with data from JSON responses
    :rtype: list
    """
    batch_url = f"{iex_url_base}stock/market/batch?"
    rs = (grequests.get(batch_url, params=payload) for payload in payloads)
    result = grequests.map(rs)
    try:
        outputs = [r.json() for r in result]
    except AttributeError:
        outputs = []
    return outputs


def iex_get_stat(batch):
    """
    :param batch: List of up to 100 symbols
    :type batch: list
    :return: Pandas DataFrame with key stats
    :rtype: Pandas DataFrame
    """
    return Stock(batch, output_format="pandas").get_key_stats().T


def get_stats(symbols):
    """
    :param symbols: List of symbols
    :type symbols: list
    :return: Pandas DataFrame with stats
    :rtype: Pandas DataFrame
    """
    with Pool() as pool:
        return pd.concat(
            pool.starmap(iex_get_stat, [[batch] for batch in split_symbols(symbols)])
        )


def iex_get_close(batch):
    """
    :param batch: List of up to 100 symbols
    :type batch: list
    :return: Pandas DataFrame with closing prices
    :rtype: Pandas DataFrame
    """
    frame = Stock(batch, output_format="pandas").get_close()
    return frame


def get_close(symbols):
    """
    :param symbols: List of symbols
    :type symbols: list
    :return: Pandas DataFrame with closing prices
    :rtype: Pandas DataFrame
    """
    with Pool() as pool:
        return pd.concat(
            pool.starmap(iex_get_close, [[batch] for batch in split_symbols(symbols)])
        )


def iex_get_volume(batch):
    """
    :param batch: List of up to 100 symbols
    :type batch: list
    :return: Pandas DataFrame with volumes of symbols
    :rtype: Pandas DataFrame
    """
    return Stock(batch, output_format="pandas").get_volume()


def get_volume(symbols):
    """
    :param symbols: List of symbols
    :type symbols: list
    :return: Pandas DataFrame with volumes of symbols
    :rtype: Pandas DataFrame
    """
    with Pool() as pool:
        return pd.concat(
            pool.starmap(iex_get_volume, [[batch] for batch in split_symbols(symbols)])
        )


def get_financials(batch_data):
    """
    :param batch_data: List of concatenated symbols
    :type batch_data: list
    :return: Dictionary of financials
    :rtype: dict
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
    :param batch_data: List of concatenated symbols
    :type batch_data: list
    :param time: Length of time (1m = 1 month, 1y = 1 year, etc.) can go up to 5y
    :type time: str
    :return: Dictionary of stock splits
    :rtype: dict
    """
    payloads = [
        {"symbols": batch, "types": "splits", "range": time} for batch in batch_data
    ]
    outputs = get_responses(payloads=payloads)
    splits = {
        symbol: outputs[outputs.index(batch_dict)][symbol]["splits"]
        for batch_dict in outputs
        for symbol in batch_dict
    }
    return splits


def get_dividends(batch_data, time="5y"):
    """
    :param batch_data: List of concatenated symbols
    :type batch_data: list
    :param time: Length of time (1m = 1 month, 1y = 1 year, etc.) can go up to 5y
    :type time: str
    :return: Dictionary of stock dividends
    :rtype: dict
    """
    payloads = [
        {"symbols": batch, "types": "dividends", "range": time} for batch in batch_data
    ]
    outputs = get_responses(payloads=payloads)
    dividends = {
        symbol: outputs[outputs.index(batch_dict)][symbol]["dividends"]
        for batch_dict in outputs
        for symbol in batch_dict
    }
    return dividends


def total_setup():
    """
    # Need to make sure the correct rtype is tuple
    :return: Total setup returns symbols, stock_scores, and batch_symbols.
    :rtype: tuple
    """
    symbols = get_symbols()
    stock_scores, batch_symbols = init_stock_scores(symbols), set_batches(symbols)
    return symbols, stock_scores, batch_symbols


def return_top(scores, metric, x):
    """
    :param scores: Pandas DataFrame with scores
    :type scores: Pandas DataFrame
    :param metric: String value for what score is desired ("Growth Score", "Value Score", "Momentum Score", "Score")
    :type metric: str
    :param x: Integer number of top stocks to return
    :type x: int
    :return: return top x number of stocks by score as Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    top = scores.nlargest(x, [metric])
    return top


def soup_it(url):
    """
    :param url: Give url for HTML code to be copied
    :type url: str
    :return: Returns parsed HTML code (to strip info from)
    :rtype: BeautifulSoup object
    """
    page = requests.get(url).text.encode("utf-8").decode("ascii", "ignore")
    soup = BeautifulSoup(page, "html.parser")
    return soup
