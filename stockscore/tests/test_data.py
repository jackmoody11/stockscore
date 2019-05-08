from stockscore.data import Stocks, return_top
import pandas as pd
import pytest

symbols = ["FB", "AAPL", "AMZN", "NFLX", "GOOGL"]
stocks = Stocks(symbols)

tdata = {
    "Score": [6, 5, 4, 3, 2],
    "Value Score": [1, 2, 3, 1, 0],
    "Growth Score": [3, 2, 0, 1, 2],
    "Momentum Score": [2, 1, 1, 1, 0],
}
tscores = pd.DataFrame(tdata, index=symbols)


def test_batches_set():
    if not len(stocks.batches) == 1:
        raise AssertionError(
            "Batch length is {}, but it should be 1.".format(
                len(stocks.batches))
        )


def test_stocks_set():
    if not stocks.stocks == symbols:
        raise AssertionError("Stocks(symbols).stocks should equal symbols")


@pytest.mark.slow
def test_get_stats():
    stocks.get_stats()
    if not isinstance(stocks.stats, pd.DataFrame):
        raise AssertionError(
            "Expected Stocks().stats object to be pandas DataFrame object"
        )
    if not len(stocks.stats) == len(stocks.stocks):
        raise AssertionError(
            "Expected Stocks().stats object to be the same length as the number of stocks"
        )


@pytest.mark.slow
@pytest.mark.skip(reason="Change in API: close data needs to be fixed")
def test_get_close():
    stocks.get_close()
    if not isinstance(stocks.close, pd.DataFrame):
        raise AssertionError(
            "Expected Stocks().close object to be pandas DataFrame object"
        )
    if not len(stocks.close) == len(stocks.stocks):
        raise AssertionError(
            "Expected Stocks().close object to be the same length as the number of stocks"
        )


@pytest.mark.slow
@pytest.mark.skip(reason="Change in API: volume data needs to be fixed")
def test_get_volume():
    stocks.get_volume()
    if not isinstance(stocks.volume, pd.DataFrame):
        raise AssertionError(
            "Expected Stocks().volume object to be pandas DataFrame object"
        )
    if not len(stocks.volume) == len(stocks.stocks):
        raise AssertionError(
            "Expected Stocks().volume object to be the same length as the number of stocks"
        )


@pytest.mark.slow
def test_get_financials():
    stocks.get_financials()
    if not isinstance(stocks.financials, dict):
        raise AssertionError("Expected Stocks().financials object to be dict")
    if not len(stocks.financials) == len(stocks.stocks):
        raise AssertionError(
            "Expected Stocks().financials object to be the same length as the number of stocks"
        )


@pytest.mark.slow
def test_get_splits():
    stocks.get_splits()
    if not isinstance(stocks.splits, dict):
        raise AssertionError("Expected Stocks().splits object to be dict")
    if not len(stocks.splits) == len(stocks.stocks):
        raise AssertionError(
            "Expected Stocks().splits object to be the same length as the number of stocks"
        )


@pytest.mark.slow
def test_get_dividends():
    stocks.get_dividends()
    if not isinstance(stocks.dividends, pd.DataFrame):
        raise AssertionError(
            "Expected Stocks().dividends object to be pandas DataFrame"
        )
    if not len(stocks.dividends) == len(stocks.stocks):
        raise AssertionError(
            "Expected Stocks().dividends object to be the same length as the number of stocks"
        )


def test_init_scores():
    stocks.init_scores()
    if not isinstance(stocks.scores, pd.DataFrame):
        raise AssertionError(
            "Expected Stocks().scores object to be pandas DataFrame")
    if not stocks.scores.eq(0).all().all():
        raise AssertionError("Expected all scores to be 0.")


def test_return_top():
    top = return_top(tscores, "Score", 2)
    if not isinstance(top, pd.DataFrame):
        raise AssertionError("return_top should return pandas DataFrame.")
    if not top.index[0] == "FB":
        raise AssertionError("Top stock is not expected stock")
