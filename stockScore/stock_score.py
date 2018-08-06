# Stock Score script created by Jack Moody 2018
#
# Other useful libraries that can be used:
# import sys
# import numpy as np

from stockScore import utils
from stockScore import technical_functions as tf
from stockScore import fundamental_functions as ff
from stockScore.graph import plot_top
import time


def score_stocks(num_stocks):
    print("Setting up stocks and scores...")
    _, stock_scores, batch_data = utils.total_setup()

    print("Fetching data dictionaries...")
    chart, stats, financials, splits, dividends = (
        utils.get_chart(batch_data),
        utils.get_stats(batch_data),
        utils.get_financials(batch_data),
        utils.get_splits(batch_data),
        utils.get_dividends(batch_data),
    )

    print("Running tests...")
    stock_scores = ff.suite(batch_data, stock_scores, dividends=dividends, financials=financials, stats=stats)
    del dividends, financials
    stock_scores = tf.suite(batch_data, stock_scores, stats=stats, splits=splits, chart=chart)
    del stats, splits, chart

    top_stocks = utils.return_top(stock_scores, num_stocks)
    plot_top(top_stocks)
    return top_stocks


if __name__ == "__main__":
    begin = time.time()
    top = score_stocks(5)
    print(f"The top {5} stocks are {top}")
    end = time.time()
    print(f"That took {end - begin} seconds")
