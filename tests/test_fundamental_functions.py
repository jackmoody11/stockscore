from stockScore import fundamental_functions as ff
from stockScore import start as start

symbols, _, batch_data = start.total_setup()
financials = start.get_financials(batch_data)


def test_dividend_test_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = ff.dividend_test(batch_data, scores)
    assert len(
        scores) >= 1000, 'At least 1000 dividend scores listed in stock_scores dictionary'


def test_dividend_test_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = ff.dividend_test(batch_data, scores)
    assert not all(score == 0 for score in scores.values())


def test_net_income_test_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = ff.net_income_test(batch_data, scores, financials=financials)
    assert len(
        scores) >= 1000, 'At least 1000 net income scores listed in stock_scores dictionary'


def test_net_income_test_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = ff.net_income_test(batch_data, scores, financials=financials)
    assert not all(score == 0 for score in scores.values())


def test_net_income_test_returns_aapl_with_pos_ni_for_all_years_given():
    """
    This test assumes that AAPL will continue to have positive net income for years to come.
    May (hopefully not) need to be updated in the future. Also assumes that 5y period is used
    for Net Income test.
    """
    scores = start.init_stock_scores(symbols)
    scores = ff.net_income_test(batch_data, scores, financials=financials)
    assert scores['AAPL'] == 4


def test_current_ratio_test_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = ff.current_ratio_test(batch_data, scores, financials=financials)
    assert len(
        scores) >= 1000, 'At least 1000 current ratio scores listed in stock_scores dictionary'


def test_current_ratio_test_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = ff.current_ratio_test(batch_data, scores, financials=financials)
    assert not all(score == 0 for score in scores.values())


def test_suite_returns_scores():
    scores = start.init_stock_scores(symbols)
    scores = ff.suite(batch_data, scores, financials=financials)
    assert len(scores) >= 1000, 'At least 1000 scores listed in stock_scores dictionary'


def test_suite_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = ff.suite(batch_data, scores, financials=financials)
    assert not all(score == 0 for score in scores.values())
