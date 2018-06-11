import technical_functions as tf
import setup

iex_url_base = "https://api.iextrading.com/1.0/"
symbols = setup.get_symbols(iex_url_base)
batch_symbols = setup.set_batches(symbols)
stock_scores = setup.init_stock_scores(symbols)


def test_moving_avg():
    scores = tf.moving_avg_test(batch_symbols, iex_url_base, stock_scores)
    assert len(scores) >= 100, 'At least 100 scores listed in stock_scores dictionary'
