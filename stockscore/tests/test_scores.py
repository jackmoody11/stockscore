from stockscore.scores import Scores
import pandas as pd
import pytest

symbols = ["FB", "AAPL", "AMZN", "NFLX", "GOOGL"]
stock_scores = Scores(symbols)


def test_moving_avg_screen_is_df():
    stock_scores.init_scores()
    stock_scores.moving_avg_screen()
    if not isinstance(stock_scores.scores, pd.DataFrame):
        raise AssertionError(
            "Moving Avg. Screen should return pandas DataFrame")


@pytest.mark.skip(reason="Change in API: volume data needs to be fixed")
def test_trading_volume_screen_is_df():
    stock_scores.init_scores()
    stock_scores.trading_volume_screen()
    if not isinstance(stock_scores.scores, pd.DataFrame):
        raise AssertionError(
            "Trading Vol. Screen should return pandas DataFrame")


def test_dividend_test_returns_scores():
    stock_scores.init_scores()
    stock_scores.dividend_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


def test_net_income_test_returns_scores():
    stock_scores.init_scores()
    stock_scores.net_income_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


def test_net_income_test_returns_aapl_with_pos_ni_for_all_years_given():
    """
    This test assumes that AAPL will continue to have positive net income for years to come.
    May (hopefully not) need to be updated in the future. Also assumes that 5y period is used
    for Net Income test.
    """
    stock_scores.init_scores()
    stock_scores.net_income_screen()
    if stock_scores.scores.loc["AAPL"]["Value Score"] == 0:
        raise AssertionError(
            "AAPL was not given a positive score for net income")


def test_current_ratio_test_returns_scores():
    stock_scores.init_scores()
    stock_scores.current_ratio_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


def test_p_to_b_test_returns_scores():
    stock_scores.init_scores()
    stock_scores.current_ratio_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


@pytest.mark.skip(reason="Change in API: close data needs to be fixed")
def test_pe_ratio_test_returns_scores():
    stock_scores.init_scores()
    stock_scores.pe_ratio_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


def test_profit_margin_returns_scores():
    stock_scores.init_scores()
    stock_scores.profit_margin_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


@pytest.mark.skip(reason="Change in API: volume and close data needs to be fixed")
def test_suite_returns_scores():
    stock_scores.init_scores()
    stock_scores.score()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


def test_moving_avg_returns_scores():
    stock_scores.init_scores()
    stock_scores.moving_avg_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


def test_splits_returns_scores():
    stock_scores.init_scores()
    stock_scores.splits_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")


@pytest.mark.skip(reason="Change in API: volume data needs to be fixed")
def test_trading_volume_test_returns_scores():
    stock_scores.init_scores()
    stock_scores.trading_volume_screen()
    if not len(stock_scores.scores) == len(symbols):
        raise AssertionError("Number of scores should equal number of symbols")
