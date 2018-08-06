from stockScore import technical_functions as tf
from stockScore import start as start
# Set constants
from .utils import symbols as symbols
from .utils import batch_data as batch_data
from .utils import stats as stats
from .utils import splits as splits
from .utils import chart as chart


def test_moving_avg_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = tf.moving_avg_test(batch_data, scores, stats=stats)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 moving avg scores listed in stock_scores dictionary')


def test_moving_avg_not_all_zero():

    scores = start.init_stock_scores(symbols)
    scores = tf.moving_avg_test(batch_data, scores, stats=stats)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Moving average test returning all scores as zero')


def test_splits_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = tf.split_test(batch_data, scores, splits=splits)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 moving avg scores listed in stock_scores dictionary')


def test_splits_not_all_zero():

    scores = start.init_stock_scores(symbols)
    scores = tf.split_test(batch_data, scores, splits=splits)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Splits test returning all scores as zero')


def test_trading_volume_test_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = tf.trading_volume_test(batch_data, scores, chart=chart)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 dividend scores listed in stock_scores dictionary')


def test_trading_volume_test_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = tf.trading_volume_test(batch_data, scores, chart=chart)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Trading volume test returning all zero values')


def test_suite_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = tf.suite(batch_data, scores, stats=stats, splits=splits)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Technical suite returning all scores as zero')


def test_suite_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = tf.suite(batch_data, scores, stats=stats, splits=splits)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 moving avg scores listed in stock_scores dictionary')
