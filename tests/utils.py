from stockscore import utils

symbols, _, batch_data = utils.total_setup()
financials = utils.get_financials(batch_data)
stats = utils.get_stats(symbols)
splits = utils.get_splits(batch_data)
dividends = utils.get_dividends(batch_data)
volume = utils.get_volume(symbols)
close = utils.get_close(symbols)
