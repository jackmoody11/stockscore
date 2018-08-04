from stockScore import statistical_functions as sf
from stockScore import start as start
from .utils import symbols as symbols
from .utils import batch_data as batch_data
from .utils import stats as stats
from .utils import chart as chart


def test_trading_volume_test_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = sf.trading_volume_test(batch_data, scores, chart=chart)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 dividend scores listed in stock_scores dictionary')


def test_trading_volume_test_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = sf.trading_volume_test(batch_data, scores, chart=chart)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Trading volume test returning all zero values')


def test_p_to_b_test_returns_scores():
    scores = start.init_stock_scores(symbols)
    scores = sf.p_to_b_test(batch_data, scores, stats=stats)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 scores for price/book test')


def test_p_to_b_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = sf.p_to_b_test(batch_data, scores)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Price to book test returning all scores as zero')


def test_pe_ratio_test_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = sf.pe_ratio_test(batch_data, scores, chart=chart, stats=stats)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 P/E ratio scores listed in stock_scores dictionary')


def test_pe_ratio_test_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = sf.pe_ratio_test(batch_data, scores, chart=chart, stats=stats)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Price to earnings test returning all scores as zero')


def test_suite_returns_scores():
    scores = start.init_stock_scores(symbols)
    scores = sf.suite(batch_data, scores, chart=chart, stats=stats)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 scores for suite test')


def test_suite_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = sf.suite(batch_data, scores, chart=chart, stats=stats)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Statistical test suite returning all scores as zero')
