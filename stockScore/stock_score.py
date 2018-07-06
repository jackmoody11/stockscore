# Stock Score script created by Jack Moody 2018
#
# For each stock test, expect to spend about 20 seconds per test used
#
# Other useful libraries that can be used:
# time
# numpy

from stockScore import start as start
from stockScore import technical_functions as tf
from stockScore import statistical_functions as sf
from stockScore import fundamental_functions as ff
import time

start_time = time.time()

symbols, stock_scores, batch_symbols = start.total_setup()


stock_scores = ff.suite(batch_symbols, stock_scores)
stock_scores = sf.suite(batch_symbols, stock_scores)
stock_scores = tf.suite(batch_symbols, stock_scores)

top_20 = start.return_top(stock_scores, 20)

end_time = time.time()
print("The top 20 companies are", top_20)
print("That took " + str(end_time - start_time) + " seconds")
