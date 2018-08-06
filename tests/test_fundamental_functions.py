from stockScore import fundamental_functions as ff
from stockScore import utils
from .utils import symbols
from .utils import batch_data
from .utils import financials
from .utils import chart
from .utils import stats


def test_dividend_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = ff.dividend_test(batch_data, scores)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 dividend scores are not listed in stock_scores dictionary')


def test_dividend_test_not_all_zero():
    scores = utils.init_stock_scores(symbols)
    scores = ff.dividend_test(batch_data, scores)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('All scores are zero')


def test_net_income_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = ff.net_income_test(batch_data, scores, financials=financials)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 net income scores listed in stock_scores dictionary')


def test_net_income_test_not_all_zero():
    scores = utils.init_stock_scores(symbols)
    scores = ff.net_income_test(batch_data, scores, financials=financials)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('All scores returned as zero')


def test_net_income_test_returns_aapl_with_pos_ni_for_all_years_given():
    """
    This test assumes that AAPL will continue to have positive net income for years to come.
    May (hopefully not) need to be updated in the future. Also assumes that 5y period is used
    for Net Income test.
    """
    scores = utils.init_stock_scores(symbols)
    scores = ff.net_income_test(batch_data, scores, financials=financials)
    if not(scores['AAPL']):
        raise AssertionError('AAPL was not given a positive score')


def test_current_ratio_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = ff.current_ratio_test(batch_data, scores, financials=financials)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 current ratio scores listed in stock_scores dictionary')


def test_current_ratio_test_not_all_zero():
    scores = utils.init_stock_scores(symbols)
    scores = ff.current_ratio_test(batch_data, scores, financials=financials)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Current ratio test returned all zero scores')


def test_p_to_b_test_returns_scores():
    scores = utils.init_stock_scores(symbols)
    scores = ff.p_to_b_test(batch_data, scores, stats=stats)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 scores for price/book test')


def test_p_to_b_not_all_zero():
    scores = utils.init_stock_scores(symbols)
    scores = ff.p_to_b_test(batch_data, scores)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Price to book test returning all scores as zero')


def test_pe_ratio_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = ff.pe_ratio_test(batch_data, scores, chart=chart, stats=stats)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 P/E ratio scores listed in stock_scores dictionary')


def test_pe_ratio_test_not_all_zero():
    scores = utils.init_stock_scores(symbols)
    scores = ff.pe_ratio_test(batch_data, scores, chart=chart, stats=stats)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Price to earnings test returning all scores as zero')


def test_suite_returns_scores():
    scores = utils.init_stock_scores(symbols)
    scores = ff.suite(batch_data, scores, financials=financials)
    if not(len(scores) >= 1000):
        raise AssertionError('At least 1000 scores listed in stock_scores dictionary')


def test_suite_not_all_zero():
    scores = utils.init_stock_scores(symbols)
    scores = ff.suite(batch_data, scores, financials=financials)
    if all(score == 0 for score in scores.values()):
        raise AssertionError('Fundamental suite returned all scores of zero')
