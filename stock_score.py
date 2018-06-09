# Stock Score script created by Jack Moody 2018
#
# For each stock test, expect to spend about 20 seconds per test used
#
# Other useful libraries that can be used:
# time
# numpy

import setup
import technical_functions as tf
import statistical_functions as sf
import fundamental_functions as ff


iex_url_base = "https://api.iextrading.com/1.0/"
symbols = setup.get_symbols(iex_url_base)
stock_scores = setup.init_stock_scores(symbols)
batch_symbols = setup.set_batches(symbols)


stock_scores = ff.suite(batch_symbols, iex_url_base, stock_scores)
stock_scores = sf.suite(batch_symbols, iex_url_base, stock_scores)
stock_scores = tf.suite(batch_symbols, iex_url_base, stock_scores)
print(stock_scores)
