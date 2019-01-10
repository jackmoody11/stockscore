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
    stats = utils.get_stats(symbols) if stats is None else stats
    stats["perDiff"] = (
        (stats.day50MovingAvg - stats.day200MovingAvg) / stats.day200MovingAvg
    ) * 100
    stock_scores.loc[
        stats.perDiff.between(0, 5, inclusive=False), ["Value Score", "Momentum Score"]
    ] += 1
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
    splits = utils.get_splits(batch_data, time=time) if splits is None else splits
    for symbol, _ in stock_scores.iterrows():
        try:
            symbol_splits = splits[symbol]
            num_splits = len(symbol_splits)
            split_ratios = [symbol_splits[i]["ratio"] for i in range(num_splits)]
            if num_splits > 0 and all(split_ratios[i] < 1 for i in range(num_splits)):
                # Stocks that split so that you get 7 stock for every 1 you own may indicate good future prospects
                # They probably feel good about future prospects and want to allow more
                # investors to invest in them
                pts = num_splits
                stock_scores.loc[symbol, ["Momentum Score", "Growth Score"]] += pts
                # print(
                #     f"{symbol} went up by {pts} -- split bullishly {num_splits} times in past {time}"
                # )
            elif num_splits > 0:
                # Stocks that split so that you get 1 stock for every 7 you own may indicate poor future prospects
                # They may be worried about staying in the market
                # and need to maintain some minimum price to keep trading
                pts = sum(1 for i in range(num_splits) if split_ratios[i] > 1)
                stock_scores.loc[symbol, ["Momentum Score", "Growth Score"]] -= pts
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
    volume = utils.get_volume(symbols) if volume is None else volume
    stock_scores.loc[
        volume.latestVolume >= 100000, ["Value Score", "Momentum Score"]
    ] += 1
    stock_scores.loc[
        volume.latestVolume <= 50000, ["Value Score", "Momentum Score"]
    ] -= 1
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
