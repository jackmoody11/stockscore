from stockscore import utils


def moving_avg_test(symbols, stock_scores, stats=None):
    """
    :param symbols: List of symbols
    :type symbols: list
    :param stock_scores: Pandas DataFrame with scores
    :type stock_scores: Pandas DataFrame
    :param stats: Pandas DataFrame with key stats from IEX API
    :type stats: Pandas DataFrame
    :return: Returns an updated stock_score Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    if stats is None:
        stats = utils.get_stats(symbols)
    stats["perDiff"] = (
        (stats.day50MovingAvg - stats.day200MovingAvg) / stats.day200MovingAvg
    ) * 100
    for symbol, _ in stock_scores.iterrows():
        try:
            pts = round(5 / (stats.loc[symbol]["perDiff"] + 1))
            if 0 < stats.loc[symbol]["perDiff"] < 5:
                stock_scores.loc[symbol]["Momentum Score"] += pts
                # print(
                #     f"{symbol} score went up by {pts} -- SMA 200 under SMA 50 by {per_diff}%"
                # )

        except ValueError:
            continue

    return stock_scores


def split_test(batch_data, stock_scores, splits=None, time="1y"):
    """
    :param batch_data: List of concatenated symbols
    :type batch_data: list
    :param stock_scores: Pandas DataFrame with scores
    :type stock_scores: Pandas DataFrame
    :param splits: Dictionary with all split information from IEX API
    :type splits: dict
    :param time: Time over which to see if split occurred (1d = 1 day, 1m = 1 month, 1y = 1 year, etc.)
    :type time: str
    :return: Returns updated stock_score Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    if splits is None:
        splits = utils.get_splits(batch_data, time=time)
    for symbol, _ in stock_scores.iterrows():
        try:
            symbol_splits = splits[symbol]
            num_splits = len(symbol_splits)
            split_ratios = [symbol_splits[i]["ratio"] for i in range(num_splits)]
            if num_splits > 0 and all(split_ratios[i] < 1 for i in range(num_splits)):
                # Stocks that split so that you get 7 stock for every 1 you own may indicate good future prospects
                # They probably feel good about future prospects and want to allow more investors to invest in them
                pts = num_splits
                stock_scores.loc[symbol]["Momentum Score"] += pts
                # print(
                #     f"{symbol} went up by {pts} -- split bullishly {num_splits} times in past {time}"
                # )
            elif num_splits > 0:
                # Stocks that split so that you get 1 stock for every 7 you own may indicate poor future prospects
                # They may be worried about staying in the market
                # and need to maintain some minimum price to keep trading
                pts = sum(1 for i in range(num_splits) if split_ratios[i] > 1)
                stock_scores.loc[symbol]["Momentum Score"] -= pts
                # print(
                #     f"{symbol} went down by {pts} -- split bearishly {pts} times in past {time}"
                # )

        except ValueError:
            continue

    return stock_scores


def trading_volume_test(symbols, stock_scores, volume=None):
    """
    :param symbols: List of symbols
    :type symbols: list
    :param stock_scores: Pandas DataFrame with scores
    :type stock_scores: Pandas DataFrame
    :param volume: Pandas DataFrame with latest volume of symbols
    :type volume: Pandas DataFrame
    :return: Returns updated stock_scores Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    if volume is None:
        volume = utils.get_volume(symbols)

    for symbol, _ in volume.iterrows():
        try:
            latest_volume = volume.loc[symbol]["latestVolume"]
            if latest_volume >= 100000:
                stock_scores.loc[symbol]["Momentum Score"] += 1
                stock_scores.loc[symbol]["Value Score"] += 1
                # print(f'{symbol} score went up by {1} -- Volume over 100,000')
            elif latest_volume >= 50000:
                pass
            else:
                stock_scores.loc[symbol]["Momentum Score"] -= 1
                stock_scores.loc[symbol]["Value Score"] -= 1
        except (KeyError, TypeError, IndexError):
            continue  # If no value, assume data is incomplete and do not penalize

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


def suite(symbols, batch_data, stock_scores, stats=None, splits=None, volume=None):
    """
    :param symbols: List of symbols
    :type symbols: list
    :param batch_data: List of concatenated symbols
    :type batch_data: list
    :param stock_scores: Pandas DataFrame with scores
    :type stock_scores: Pandas DataFrame
    :param stats: Dictionary with key stats from IEX
    :type stats: dict
    :param splits: Dictionary with all splits information from IEX
    :type splits: dict
    :param volume: Pandas DataFrame with latest volume for symbols
    :type volume: Pandas DataFrame
    :return: Returns an updated stock_score Pandas DataFrame
    :rtype: Pandas DataFrame
    """
    stock_scores = moving_avg_test(symbols, stock_scores, stats=stats)
    stock_scores = split_test(batch_data, stock_scores, splits=splits)
    stock_scores = trading_volume_test(symbols, stock_scores, volume=volume)
    return stock_scores
