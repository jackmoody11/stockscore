# Stock Score script created by Jack Moody 2018
#
# Other useful libraries that can be used:
# import sys
# import numpy as np

from stockScore import start as start
from stockScore import technical_functions as tf
from stockScore import statistical_functions as sf
from stockScore import fundamental_functions as ff
import time


def score_stocks(num_stocks):
    print("Setting up stocks and scores...")
    symbols, stock_scores, batch_data = start.total_setup()

    print("Fetching data dictionaries...")
    chart, stats, financials, splits, dividends = (
        start.get_chart(batch_data),
        start.get_stats(batch_data),
        start.get_financials(batch_data),
        start.get_splits(batch_data),
        start.get_dividends(batch_data),
    )

    print("Running tests...")
    stock_scores = ff.suite(
        batch_data, stock_scores, dividends=dividends, financials=financials
    )
    del financials, dividends
    stock_scores = sf.suite(batch_data, stock_scores, stats=stats, chart=chart)
    del chart
    stock_scores = tf.suite(batch_data, stock_scores, stats=stats, splits=splits)
    del stats, splits

    top_stocks = start.return_top(stock_scores, num_stocks)
    return top_stocks


if __name__ == "__main__":
    top = score_stocks(20)
    print(f"The top {20} stocks are {top}")
