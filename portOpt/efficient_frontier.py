from stockScore import stock_score
import datetime
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import iexfinance as iex

symbols = ['AAPL', 'TSLA', 'F', 'GM', 'FB', 'JPM']
new_symbols = symbols.pop(-1)
start = datetime.date(2016, 4, 7)
end = datetime.date(2018, 7, 20)


for symbol in new_symbols:
    stock_prices = iex.get_historical_data(symbols, start=start, end=end, output_format="pandas")[symbol]
    stock_prices = pd.DataFrame(stock_prices, columns=['open'])
    stock_prices.columns = [symbol]
    prices = pd.concat(stock_prices)
print(prices)
