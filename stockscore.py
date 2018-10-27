# Stock Score script created by Jack Moody 2018
#
# Other useful libraries that can be used:
# import sys
# import numpy as np

from stockscore import utils
from stockscore import technical_screens as tf
from stockscore import fundamental_screens as ff
from stockscore.graph import plot_top
import time


def score_stocks(num_stocks):
    print("Setting up stocks and scores...")
    symbols, stock_scores, batch_data = utils.total_setup()

    print("Fetching data dictionaries...")
    volume, close, stats, financials, splits, dividends = (
        utils.get_volume(symbols),
        utils.get_close(symbols),
        utils.get_stats(symbols),
        utils.get_financials(batch_data),
        utils.get_splits(batch_data),
        utils.get_dividends(batch_data),
    )

    print("Running screens...")
    stock_scores = ff.suite(
        symbols,
        batch_data,
        stock_scores,
        dividends=dividends,
        financials=financials,
        stats=stats,
        close=close,
    )
    del dividends, financials, close  # Clear up memory space
    stock_scores = tf.suite(
        symbols, batch_data, stock_scores, stats=stats, splits=splits, volume=volume
    )
    del stats, splits, volume  # Clear up memory space
    stock_scores["Score"] = stock_scores.sum(axis=1)
    top_stocks = utils.return_top(
        stock_scores, "Score", num_stocks
    )  # Return top scoring stocks
    return top_stocks


# Run stock screening
if __name__ == "__main__":
    # Timer starts
    begin = time.time()
    # Choose number of top stocks you want to see
    stock_count = 10
    # Run screens to find top stocks
    top = score_stocks(stock_count)
    stocks = list(top.index)
    print(f"The top {stock_count} stocks are {stocks}")
    # End timer
    end = time.time()
    print(f"That took {end - begin:.2f} seconds")
    # Plot top stocks in bar chart
    plot_top(top)
