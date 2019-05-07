# Modules
import grequests
import pandas as pd
import numpy as np
from iexfinance.stocks import Stock
from multiprocessing import Pool
iex_url_base = "https://api.iextrading.com/1.0/"


def return_top(scores, metric, x=None):
    """

    Args:
      scores(pandas.DataFrame): pandas.DataFrame with scores
      metric(str): string value for what score is desired
      ("Growth Score", "Value Score", "Momentum Score", "Score")
      x(int, optional): integer number of top stocks to return (Default value = None)

    Returns:
      pandas.DataFrame: top x number of stocks by score as pandas.DataFrame

    """
    if x is not None:
        return scores.nlargest(x, [metric])
    else:
        return scores.nlargest(len(scores), [metric])


class Stocks:
    def __init__(self, stocks=None):
        """
        Args:
          stocks(list): list of stocks to be included in analysis

        Returns:
        """
        self.stocks = stocks
        self.batches = [stocks[i: i + 100]
                        for i in range(0, len(stocks), 100)]
        if stocks is not None:
            self.string_batches = [
                ",".join(stocks[i: i + 99]) for i in range(0, len(stocks), 99)
            ]
        else:
            raise "At least one stock ticker must be given."
        self.scores = None
        self.stats = None
        self.close = None
        self.volume = None
        self.financials = None
        self.splits = None
        self.dividends = None

    def __str__(self):
        return ('Stocks: {stocks}'
                'Batches: {batches}').format(**self.__dict__)

    def __repr__(self):
        return ('Stocks(stocks={stocks},'
                'batches={batches},'
                'scores={scores},'
                'stats={stats},'
                'close={close},'
                'volume={volume},'
                'financials={financials},'
                'splits={splits},'
                'dividends={dividends}').format(**self.__dict__)

    @staticmethod
    def iex_get_stat(batch):
        """

        Args:
          batch(list): list of up to 100 symbols

        Returns:
          pandas.DataFrame: pandas.DataFrame with key stats

        """
        return Stock(batch, output_format="pandas").get_key_stats().T

    def get_stats(self):
        """

        Args:

        Returns:
          pandas.DataFrame: pandas.DataFrame with stats

        """
        with Pool() as pool:
            self.stats = pd.concat(
                pool.starmap(self.iex_get_stat, [[batch]
                                                 for batch in self.batches])
            )

    @staticmethod
    def iex_get_close(batch):
        """

        Args:
          batch(list): List of up to 100 symbols

        Returns:
          pandas.DataFrame: pandas.DataFrame with closing prices

        """
        return Stock(batch, output_format="pandas").get_close()

    def get_close(self):
        """

        Args:

        Returns:
          pandas.DataFrame: pandas.DataFrame with closing prices

        """
        with Pool() as pool:
            self.close = pd.concat(
                pool.starmap(self.iex_get_close, [
                             [batch] for batch in self.batches])
            )

    @staticmethod
    def iex_get_volume(batch):
        """

        Args:
          batch(list): List of up to 100 symbols

        Returns:
          pandas.DataFrame: pandas.DataFrame with volumes of symbols

        """
        return Stock(batch, output_format="pandas").get_volume()

    def get_volume(self):
        """

        Args:

        Returns:
          pandas.DataFrame: pandas.DataFrame with volumes of symbols

        """
        with Pool() as pool:
            self.volume = pd.concat(
                pool.starmap(self.iex_get_volume, [
                             [batch] for batch in self.batches])
            )

    @staticmethod
    def get_responses(payloads):
        """

        Args:
          payloads(list): list of payloads for GET request

        Returns:
          list: list of dictionaries with data from JSON responses

        """
        batch_url = "{base}stock/market/batch?".format(base=iex_url_base)
        rs = (grequests.get(batch_url, params=payload) for payload in payloads)
        result = grequests.map(rs)
        try:
            outputs = [r.json() for r in result]
        except AttributeError:
            outputs = []
        return outputs

    def get_financials(self):
        """

        Args:

        Returns:
          dict: dictionary with financial information for stocks

        """
        payloads = [
            {"symbols": batch, "types": "financials"} for batch in self.string_batches
        ]
        outputs = self.get_responses(payloads=payloads)
        financials = {
            symbol: outputs[outputs.index(batch_dict)][symbol]
            for batch_dict in outputs
            for symbol in batch_dict
        }
        self.financials = financials

    def get_splits(self, time="1y"):
        """

        Args:
          time:  (Default value = "1y")

        Returns:

        """
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
        """

        Args:
          time:  (Default value = "5y")

        Returns:

        """
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
            "count": [
                len(v) if all(isinstance(i["amount"], (float))
                              for i in v) else 0
                for _, v in div_json.items()
            ],
            "amount": [
                [div_json[k][i]["amount"] for i in range(len(div_json[k]))]
                for k, _ in div_json.items()
            ],
        }
        self.dividends = pd.DataFrame(data=data, index=div_json.keys())

    def init_scores(self):
        """ """
        columns = ["Score", "Value Score", "Growth Score", "Momentum Score"]
        self.scores = pd.DataFrame(
            np.zeros((len(self.stocks), len(columns))),
            index=self.stocks,
            columns=columns,
        )
