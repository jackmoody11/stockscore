# Modules
from bs4 import BeautifulSoup
import grequests
import requests
import pandas as pd
import numpy as np
import iexfinance
from multiprocessing import Pool

iex_url_base = "https://api.iextrading.com/1.0/"


def get_symbols():
    """
    :return: gets all symbols(tickers) from IEX API
    :rtype: list
    """
    symbols_json = iexfinance.get_available_symbols()
    symbols = [symbol["symbol"] for symbol in symbols_json if symbol["type"] == "cs"]
    return symbols


class Stocks:
    def __init__(self, stocks=None):
        """
        :param stocks: list of stocks to be included in analysis
        :type stocks: list
        """
        self.stocks = stocks
        self.batches = [self.stocks[i : i + 99] for i in range(0, len(self.stocks), 99)]
        if stocks:
            self.string_batches = [
                ",".join(stocks[i : i + 99]) for i in range(0, len(self.stocks), 99)
            ]
        else:
            self.string_batches = []
        self.scores = None
        self.stats = None
        self.close = None
        self.volume = None
        self.financials = None
        self.splits = None
        self.dividends = None

    # Add __repr__ and __str__ methods

    @staticmethod
    def iex_get_stat(batch):
        """
        :param batch: list of up to 100 symbols
        :type batch: list
        :return: pandas data frame with key stats
        :rtype: pandas data frame
        """
        return iexfinance.Stock(batch, output_format="pandas").get_key_stats().T

    def get_stats(self):
        """
        :return: pandas data frame with stats
        :rtype: pandas data frame
        """
        if not self.stats:
            with Pool() as pool:
                self.stats = pd.concat(
                    pool.starmap(self.iex_get_stat, [[batch] for batch in self.batches])
                )

    @staticmethod
    def iex_get_close(batch):
        """
        :param batch: List of up to 100 symbols
        :type batch: list
        :return: pandas data frame with closing prices
        :rtype: pandas data frame
        """
        return iexfinance.Stock(batch, output_format="pandas").get_close()

    def get_close(self):
        """
        :return: pandas data frame with closing prices
        :rtype: pandas data frame
        """
        if not self.close:
            with Pool() as pool:
                self.close = pd.concat(
                    pool.starmap(
                        self.iex_get_close, [[batch] for batch in self.batches]
                    )
                )

    @staticmethod
    def iex_get_volume(batch):
        """
        :param batch: List of up to 100 symbols
        :type batch: list
        :return: pandas data frame with volumes of symbols
        :rtype: pandas data frame
        """
        return iexfinance.Stock(batch, output_format="pandas").get_volume()

    def get_volume(self):
        """
        :return: pandas data frame with volumes of symbols
        :rtype: pandas data frame
        """
        if not self.volume:
            with Pool() as pool:
                self.volume = pd.concat(
                    pool.starmap(
                        self.iex_get_volume, [[batch] for batch in self.batches]
                    )
                )

    @staticmethod
    def get_responses(payloads):
        """
        :param payloads: list of payloads for GET request
        :type payloads: list
        :return: list of dictionaries with data from JSON responses
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

    def get_financials(self):
        """
        :return: dictionary with financial information for stocks
        :rtype: dict
        """
        if not self.financials:
            payloads = [
                {"symbols": batch, "types": "financials"}
                for batch in self.string_batches
            ]
            outputs = self.get_responses(payloads=payloads)
            financials = {
                symbol: outputs[outputs.index(batch_dict)][symbol]
                for batch_dict in outputs
                for symbol in batch_dict
            }
            self.financials = financials

    def get_splits(self, time="1y"):
        if not self.splits:
            payloads = [
                {"symbols": batch, "types": "splits", "range": time}
                for batch in self.string_batches
            ]
            outputs = self.get_responses(payloads=payloads)
            self.splits = {
                symbol: outputs[outputs.index(batch_dict)][symbol]["splits"]
                for batch_dict in outputs
                for symbol in batch_dict
            }

    def get_dividends(self, time="5y"):
        if not self.dividends:
            payloads = [
                {"symbols": batch, "types": "dividends", "range": time}
                for batch in self.string_batches
            ]
            outputs = self.get_responses(payloads=payloads)
            div_json = {
                symbol: outputs[outputs.index(batch_dict)][symbol]["dividends"]
                for batch_dict in outputs
                for symbol in batch_dict
            }
            data = {
                "count": [len(v) for _, v in div_json.items()],
                "amount": [
                    [div_json[k][i]["amount"] for i in range(len(div_json[k]))]
                    for k, _ in div_json.items()
                ],
            }
            self.dividends = pd.DataFrame(data=data, index=div_json.keys())

    def init_scores(self):
        columns = ["Score", "Value Score", "Growth Score", "Momentum Score"]
        self.scores = pd.DataFrame(
            np.zeros((len(self.stocks), len(columns))),
            index=self.stocks,
            columns=columns,
        )


def return_top(scores, metric, x):
    """
    :param scores: pandas data frame with scores
    :type scores: pandas data frame
    :param metric: string value for what score is desired ("Growth Score", "Value Score", "Momentum Score", "Score")
    :type metric: str
    :param x: integer number of top stocks to return
    :type x: int
    :return: top x number of stocks by score as pandas data frame
    :rtype: pandas data frame
    """
    top = scores.nlargest(x, [metric])
    return top


def soup_it(url):
    """
    :param url: give url for HTML code to be copied
    :type url: str
    :return: parsed HTML code (to strip info from)
    :rtype: BeautifulSoup object
    """
    page = requests.get(url).text.encode("utf-8").decode("ascii", "ignore")
    soup = BeautifulSoup(page, "html.parser")
    return soup
