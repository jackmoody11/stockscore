from stockScore import utils
# import numpy as np


def moving_avg_test(batch_data, stock_scores, stats=None):

    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Dictionary with all statistical information from IEX API (see get_stats in utils
    module for more info.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that moving_avg_test() can return updated stock scores.
    """
    if stats is None:
        stats = utils.get_stats(batch_data)

    for symbol in stock_scores:
        try:
            base = stats[symbol]["stats"]
            avg_50 = base["day50MovingAvg"]
            avg_200 = base["day200MovingAvg"]
            per_diff = ((avg_50 - avg_200) / avg_200) * 100
            pts = round(5 / (per_diff + 1))
            if 0 < per_diff < 2:
                stock_scores[symbol] += pts
                # print(
                #     f"{symbol} score went up by {pts} -- SMA 200 under SMA 50 by {per_diff}%"
                # )
            elif 2 < per_diff < 5:
                stock_scores[symbol] += pts
                # print(
                #     f"{symbol} score went up by {pts} -- SMA 200 under SMA 50 by {per_diff}%"
                # )

        except (KeyError, TypeError):
            continue

    return stock_scores


def split_test(batch_data, stock_scores, splits=None, time="5y"):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param splits: Dictionary with all split information from IEX API (see get_splits in utils
    module for more info.
    :param time: Time over which to see if split occurred. (1d = 1 day, 1m = 1 month, 1y = 1 year)
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that moving_avg_test() can return updated stock scores.
    """
    if splits is None:
        splits = utils.get_splits(batch_data, time=time)
    for symbol in stock_scores:
        try:
            symbol_splits = splits[symbol]["splits"]
            num_splits = len(symbol_splits)
            split_ratios = [symbol_splits[i]["ratio"] for i in range(num_splits)]
            if num_splits > 0 and all(split_ratios[i] < 1 for i in range(num_splits)):
                # Stocks that split so that you get 7 stock for every 1 you own may indicate good future prospects
                # They probably feel good about future prospects and want to allow more investors to invest in them
                pts = num_splits
                stock_scores[symbol] += pts
                # print(
                #     f"{symbol} went up by {pts} -- split bullishly {num_splits} times in past {time}"
                # )
            elif num_splits > 0:
                # Stocks that split so that you get 1 stock for every 7 you own may indicate poor future prospects
                # They may be worried about staying in the market
                # and need to maintain some minimum price to keep trading
                pts = sum(1 for i in range(num_splits) if split_ratios[i] > 1)
                stock_scores[symbol] -= pts
                # print(
                #     f"{symbol} went down by {pts} -- split bearishly {pts} times in past {time}"
                # )

        except (TypeError, KeyError):
            continue

    return stock_scores


def trading_volume_test(batch_data, stock_scores, chart=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param chart: Defaults as None, but can be set to value to speed up performance if running suite
    or multiple tests at once.
    :return: Returns updated stock_score dictionary. Make sure to set stock_score to the function
    so that trading_volume_test() returns updated stock scores.
    """
    if chart is None:
        chart = utils.get_chart(batch_data)

    for symbol in chart:
        try:
            latest_volume = chart[symbol]["chart"][0]["volume"]
            if latest_volume >= 100000:
                stock_scores[symbol] += 1
                # print(f'{symbol} score went up by {1} -- Volume over 100,000')
            elif latest_volume >= 50000:
                pass
            else:
                stock_scores[symbol] -= 1
                # print(f'{symbol} score went down by {1} -- Volume under 50,000')
        except (KeyError, TypeError, IndexError):
            continue  # If no chart, assume data is incomplete - no penalty for symbol if data incomplete

    return stock_scores
# In progress
# def rsi_test(batch_data, stock_scores, chart=None):
#     if chart is None:
#         chart = utils.get_chart(batch_data, time='1m')
#
#     for symbol in chart:
#         try:
#             change_pct = list()
#             rsi = list()
#             for day in range(len(chart[symbol]['chart'])):
#                 change_pct.insert(0, chart[symbol]['chart'][day]['changePercent'])
#             for i in range(len(change_pct)):
#                 avg_gain = np.average([change_pct[j] for j in range(i, i+14) if change_pct[j] >= 0])
#                 avg_loss = np.average([change_pct[j] for j in range(i, i+14) if change_pct[j] < 0])
#                 rs = avg_gain/avg_loss
#                 val = 100 - 100/(1+rs)
#                 rsi.insert(val)
#         except (KeyError, TypeError, IndexError):
#             continue  # If no chart, assume data is incomplete - no penalty for symbol if data incomplete
#
#     return stock_scores


def suite(batch_data, stock_scores, stats=None, splits=None, chart=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Dictionary with all statistical information from IEX API (see get_stats in utils
    module for more info.
    :param splits: Dictionary with all splits information from IEX API (see get_splits in utils
    module for more info.
    :param chart: Dictionary with price and volume information from IEX API (see get_chart in utils
    module for more info.
    :return: Returns an updated stock_score dictionary that runs all functions
    in technical_functions module. Make sure to set stock_score to the function
    so that suite() can return updated stock scores.
    """
    stock_scores = moving_avg_test(batch_data, stock_scores, stats=stats)
    stock_scores = split_test(batch_data, stock_scores, splits=splits)
    stock_scores = trading_volume_test(batch_data, stock_scores, chart=chart)
    return stock_scores
