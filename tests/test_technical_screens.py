from stockscore import technical_screens as ts
from stockscore import utils
# Set constants
from .utils import symbols
from .utils import batch_data
from .utils import stats
from .utils import splits
from .utils import chart


def test_moving_avg_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = ts.moving_avg_test(batch_data, scores, stats=stats)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 moving avg scores listed in stock_scores dictionary')


def test_moving_avg_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = ts.moving_avg_test(batch_data, scores, stats=stats)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Moving average test returning all scores as zero')


def test_splits_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = ts.split_test(batch_data, scores, splits=splits)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 moving avg scores listed in stock_scores dictionary')


def test_splits_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = ts.split_test(batch_data, scores, splits=splits)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Splits test returning all scores as zero')


def test_trading_volume_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = ts.trading_volume_test(batch_data, scores, chart=chart)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 dividend scores listed in stock_scores dictionary')


def test_trading_volume_test_not_all_zero():
    scores = utils.init_stock_scores(symbols)
    scores = ts.trading_volume_test(batch_data, scores, chart=chart)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Trading volume test returning all zero values')


def test_suite_not_all_zero():
    scores = utils.init_stock_scores(symbols)
    scores = ts.suite(batch_data, scores, stats=stats, splits=splits)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Technical suite returning all scores as zero')


def test_suite_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = ts.suite(batch_data, scores, stats=stats, splits=splits)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 moving avg scores listed in stock_scores dictionary')
