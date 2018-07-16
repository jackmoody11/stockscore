from stockScore import start


def moving_avg_test(batch_data, stock_scores, stats=None):

    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Defaults as None, but can be set to value to speed up performance if running suite
    or multiple tests at once.
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that moving_avg_test() can return updated stock scores.
    """
    if stats is None:
        stats = start.get_stats(batch_data)

    for symbol in stock_scores:
        if stats.get(symbol) and stats[symbol].get('stats'):
            base = stats[symbol]['stats']
            if base.get('day200MovingAvg') and base.get('day50MovingAvg'):
                avg_50 = base['day50MovingAvg']
                avg_200 = base['day200MovingAvg']
                per_diff = ((avg_50 - avg_200) / avg_200) * 100
                score = per_diff
                if 0 < per_diff < 2:
                    pts = round(5 / (score + 1))
                    stock_scores[symbol] += pts
                    print(symbol + " score went up by " + str(pts) + " -- SMA 200 under SMA 50 by " + str(
                        per_diff) + "%")
                elif 2 < per_diff < 5:
                    pts = round(5 / score)
                    stock_scores[symbol] += pts
                    print(symbol + " score went up by " + str(pts) + " -- SMA 200 under SMA 50 by " + str(
                        per_diff) + "%")

    return stock_scores


def suite(batch_data, stock_scores, stats=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Defaults as None, but can be set to value to speed up performance if running suite
    or multiple tests at once.
    :return: Returns an updated stock_score dictionary that runs all functions
    in technical_functions module. Make sure to set stock_score to the function
    so that suite() can return updated stock scores.
    """
    stock_scores = moving_avg_test(batch_data, stock_scores, stats)
    return stock_scores
