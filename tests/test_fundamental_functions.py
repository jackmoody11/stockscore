from stockScore import fundamental_functions as ff
from stockScore import start as start

symbols = start.get_symbols()
batch_symbols = start.set_batches(symbols)
stock_scores = start.init_stock_scores(symbols)


def test_dividend_test_returns_scores():

    scores = ff.dividend_test(batch_symbols, stock_scores)
    assert len(
        scores) >= 1000, 'At least 1000 dividend scores listed in stock_scores dictionary'


def test_net_income_test():

    scores = ff.net_income_test(batch_symbols, stock_scores)
    assert len(
        scores) >= 1000, 'At least 1000 net income scores listed in stock_scores dictionary'
