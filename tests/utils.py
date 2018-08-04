from stockScore import start as start

symbols, _, batch_data = start.total_setup()
financials = start.get_financials(batch_data)
stats = start.get_stats(batch_data)
chart = start.get_chart(batch_data)
splits = start.get_splits(batch_data)
