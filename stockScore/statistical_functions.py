from stockScore import start


def p_to_b_test(batch_data, stock_scores, stats=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Defaults as None, but can be set to value to speed up performance if running suite
    or multiple tests at once.
    :return: Returns updated stock_score dictionary. Make sure to set stock_score to the function
    so that p_to_b_test() returns updated stock scores.
    """
    if stats is None:
        stats = start.get_stats(batch_data)

    for symbol in stock_scores:
        try:
            pts = round(5 / (stats[symbol]['stats']['priceToBook'] + 0.8))
            if 0 < stats[symbol]['stats']['priceToBook'] <= 1:
                stock_scores[symbol] += pts
                print(symbol + " score went up by " +
                      str(pts) + "-- price to book between 0 and 1")
            elif 1 < stats[symbol]['stats']['priceToBook'] <= 2:
                stock_scores[symbol] += pts
                print(symbol + " score went up by " +
                      str(pts) + "-- price to book between 1 and 2")
        except (TypeError, KeyError):
            continue

    return stock_scores


# Work in progress
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
        chart = start.get_chart(batch_data)

    for symbol in chart:
        try:
            latest_volume = chart[symbol]['chart'][0]['volume']
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


def suite(batch_data, stock_scores, stats=None, chart=None):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :param stats: Defaults as None, but can be set to value to speed up performance if running suite
    or multiple tests at once.
    :param chart: Defaults as None, but can be set to value to speed up performance if running suite
    or multiple tests at once.
    :return: Returns an updated stock_score dictionary that runs all functions
    in statistical_functions module. Make sure to set stock_score to the function
    so that suite() can return updated stock scores.
    """
    stock_scores = p_to_b_test(batch_data, stock_scores, stats)
    stock_scores = trading_volume_test(batch_data, stock_scores, chart)
    return stock_scores
