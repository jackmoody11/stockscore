from stockscore import fundamental_screens as fs
from stockscore import utils
from .utils import symbols, batch_data, financials, stats, dividends, close


def test_dividend_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = fs.dividend_test(batch_data, scores)
    if not (len(scores) >= 1000):
        raise AssertionError(
            "At least 1000 dividend scores are not listed in stock scores"
        )


def test_dividend_test_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = fs.dividend_test(batch_data, scores)
    if (scores["Value Score"] == 0).all():
        raise AssertionError("All scores are zero")


def test_net_income_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = fs.net_income_test(batch_data, scores, financials=financials)
    if not (len(scores) >= 1000):
        raise AssertionError("At least 1000 net income scores listed in stock scores")


def test_net_income_test_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = fs.net_income_test(batch_data, scores, financials=financials)
    if (scores["Value Score"] == 0).all():
        raise AssertionError("All scores returned as zero")


def test_net_income_test_returns_aapl_with_pos_ni_for_all_years_given():
    """
    This test assumes that AAPL will continue to have positive net income for years to come.
    May (hopefully not) need to be updated in the future. Also assumes that 5y period is used
    for Net Income test.
    """
    scores = utils.init_stock_scores(symbols)
    scores = fs.net_income_test(batch_data, scores, financials=financials)
    if scores.loc["AAPL"]["Value Score"] == 0:
        raise AssertionError("AAPL was not given a positive score for net income")


def test_current_ratio_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = fs.current_ratio_test(batch_data, scores, financials=financials)
    if not (len(scores) >= 1000):
        raise AssertionError(
            "At least 1000 current ratio scores listed in stock scores"
        )


def test_current_ratio_test_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = fs.current_ratio_test(batch_data, scores, financials=financials)
    if (scores["Value Score"] == 0).all():
        raise AssertionError("Current ratio test returned all zero scores")


def test_p_to_b_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = fs.p_to_b_test(symbols, scores, stats=stats)
    if not (len(scores) >= 1000):
        raise AssertionError("At least 1000 scores for price/book test")


def test_p_to_b_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = fs.p_to_b_test(symbols, scores, stats=stats)
    if (scores["Value Score"] == 0).all():
        raise AssertionError("Price to book test returning all scores as zero")


def test_pe_ratio_test_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = fs.pe_ratio_test(symbols, scores, stats=stats, close=close)
    if not (len(scores) >= 1000):
        raise AssertionError("At least 1000 P/E ratio scores listed in stock scores")


def test_pe_ratio_test_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = fs.pe_ratio_test(symbols, scores, close=close, stats=stats)
    if (scores["Value Score"] == 0).all():
        raise AssertionError("Price to earnings test returning all scores as zero")


def test_profit_margin_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = fs.profit_margin_test(symbols, scores, stats=stats)
    if not (len(scores) >= 1000):
        raise AssertionError(
            "At least 1000 profit margin scores listed in stock scores"
        )


def test_profit_margin_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = fs.profit_margin_test(batch_data, scores, stats=stats)
    if (scores["Value Score"] == 0).all():
        raise AssertionError("All scores returned as zero")


def test_suite_returns_scores():

    scores = utils.init_stock_scores(symbols)
    scores = fs.suite(
        symbols,
        batch_data,
        scores,
        dividends=dividends,
        financials=financials,
        stats=stats,
    )
    if not (len(scores) >= 1000):
        raise AssertionError("At least 1000 scores listed in stock scores")


def test_suite_not_all_zero():

    scores = utils.init_stock_scores(symbols)
    scores = fs.suite(
        symbols,
        batch_data,
        scores,
        dividends=dividends,
        financials=financials,
        stats=stats,
    )
    if (scores["Value Score"] == 0).all():
        raise AssertionError("Fundamental suite returned all scores of zero")
