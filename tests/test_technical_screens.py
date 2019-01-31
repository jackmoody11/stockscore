from stockscore.scores import Scores
from stockscore.data import get_symbols

stocks = get_symbols()
stock_scores = Scores(stocks)


def test_moving_avg_returns_scores():

    stock_scores.init_scores()
    stock_scores.moving_avg_screen()
    if not (len(stock_scores.scores) >= 1000):
        raise AssertionError(
            "At least 1000 moving avg scores listed in stock_scores dictionary"
        )


def test_moving_avg_not_all_zero():

    stock_scores.init_scores()
    stock_scores.moving_avg_screen()
    if (stock_scores.scores["Momentum Score"] == 0).all():
        raise AssertionError("Moving average test returning all scores as zero")


def test_splits_returns_scores():

    stock_scores.init_scores()
    stock_scores.splits_screen()
    if not (len(stock_scores.scores) >= 1000):
        raise AssertionError(
            "At least 1000 moving avg scores listed in stock_scores dictionary"
        )


def test_splits_not_all_zero():
    stock_scores.init_scores()
    stock_scores.splits_screen()
    if (stock_scores.scores["Momentum Score"] == 0).all():
        raise AssertionError("Splits test returning all scores as zero")


def test_trading_volume_test_returns_scores():
    stock_scores.init_scores()
    stock_scores.trading_volume_screen()
    if not (len(stock_scores.scores) >= 1000):
        raise AssertionError(
            "At least 1000 dividend scores listed in stock_scores dictionary"
        )


def test_trading_volume_test_not_all_zero():
    stock_scores.init_scores()
    stock_scores.trading_volume_screen()
    if (stock_scores.scores["Momentum Score"] == 0).all():
        raise AssertionError("Trading volume test returning all zero values")
