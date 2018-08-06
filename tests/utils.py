from stockScore import utils

symbols, _, batch_data = utils.total_setup()
financials = utils.get_financials(batch_data)
stats = utils.get_stats(batch_data)
chart = utils.get_chart(batch_data)
splits = utils.get_splits(batch_data)
