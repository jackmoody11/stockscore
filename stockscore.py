"""
Scores thousands of stocks and returns top stocks along with breakdown by score.
Score is broken down into 3 categories: value, momentum, and growth. The sum of these
3 scores gives the total score.
"""

from stockscore.data import get_symbols
from stockscore.scores import Scores
from stockscore.graph import plot_top
import time


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
    return scores.nlargest(x, [metric])


def score_stocks(num_stocks):
    print("Fetching symbols...")
    symbols = get_symbols()
    print("Fetching data...")
    score_obj = Scores(symbols)
    print("Scoring...")
    score_obj.score()
    return return_top(score_obj.scores, "Score", num_stocks)


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
