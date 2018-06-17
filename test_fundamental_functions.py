import fundamental_functions as ff
import setup

iex_url_base = "https://api.iextrading.com/1.0/"
symbols = setup.get_symbols(iex_url_base)
batch_symbols = setup.set_batches(symbols)
stock_scores = setup.init_stock_scores(symbols)


def test_dividend_test_returns_scores():
    scores = ff.dividend_test(batch_symbols, stock_scores)
    assert len(scores) >= 100, 'At least 100 dividend scores listed in stock_scores dictionary'

def test_dividend_test_shows_apple_paying_dividend():
    del scores
    scores = ff.dividend_test(batch_symbols, stock_scores)
    assert scores['AAPL'] == 1

def test_net_income_test():
    scores = ff.net_income_test(batch_symbols, stock_scores)
    assert len(scores) >= 100, 'At least 100 net income scores listed in stock_scores dictionary'
