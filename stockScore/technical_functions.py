from stockScore import start


def moving_avg_test(batch_data, stock_scores, stats=None):

    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Dictionary with all statistical information from IEX API (see get_stats in start
    module for more info.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that moving_avg_test() can return updated stock scores.
    """
    if stats is None:
        stats = start.get_stats(batch_data)

    for symbol in stock_scores:
        try:
            base = stats[symbol]['stats']
            avg_50 = base['day50MovingAvg']
            avg_200 = base['day200MovingAvg']
            per_diff = ((avg_50 - avg_200) / avg_200) * 100
            pts = round(5 / (per_diff + 1))
            if 0 < per_diff < 2:
                stock_scores[symbol] += pts
                print(f'{symbol} score went up by {pts} -- SMA 200 under SMA 50 by {per_diff}%')
            elif 2 < per_diff < 5:
                stock_scores[symbol] += pts
                print(f'{symbol} score went up by {pts} -- SMA 200 under SMA 50 by {per_diff}%')

        except (KeyError, TypeError):
            continue

    return stock_scores


def split_test(batch_data, stock_scores, splits=None, time="1y"):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param splits: Dictionary with all split information from IEX API (see get_splits in start
    module for more info.
    :param time: Time over which to see if split occurred. (1d = 1 day, 1m = 1 month, 1y = 1 year)
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that moving_avg_test() can return updated stock scores.
    """
    if splits is None:
        splits = start.get_splits(batch_data, time=time)
    for symbol in stock_scores:
        try:
            symbol_splits = splits[symbol]['splits']
            split_mult = len(symbol_splits)
            if split_mult >= 1:
                pts = split_mult
                stock_scores[symbol] += pts
                print(f'{symbol} went up by {pts} -- split {split_mult} times in past {time}')

        except (TypeError, KeyError):
            continue

    return stock_scores


def suite(batch_data, stock_scores, stats=None, splits=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Dictionary with all statistical information from IEX API (see get_stats in start
    module for more info.
    :param splits: Dictionary with all splits information from IEX API (see get_splits in start
    module for more info.
    :return: Returns an updated stock_score dictionary that runs all functions
    in technical_functions module. Make sure to set stock_score to the function
    so that suite() can return updated stock scores.
    """
    stock_scores = moving_avg_test(batch_data, stock_scores, stats)
    stock_scores = split_test(batch_data, stock_scores, splits)
    return stock_scores
