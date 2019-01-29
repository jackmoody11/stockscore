"""
Scores thousands of stocks and returns top stocks along with breakdown by score.
Score is broken down into 3 categories: value, momentum, and growth. The sum of these
3 scores gives the total score.
"""

from stockscore.data import Stocks, get_symbols
from stockscore.scores import Scores
from stockscore.graph import plot_top
import time


def score_stocks():
    symbols = get_symbols()
    stks = Stocks(symbols)
    stock_scores = Scores(stks.stocks).scores
    return stock_scores


# Run stock screening
if __name__ == "__main__":
    # Timer starts
    begin = time.time()
    # Choose number of top stocks you want to see
    stock_count = 10
    # Run screens to find top stocks
    top = score_stocks()
    stocks = list(top.index)
    print(f"The top {stock_count} stocks are {stocks}")
    # End timer
    end = time.time()
    print(f"That took {end - begin:.2f} seconds")
    # Plot top stocks in bar chart
    plot_top(top)
