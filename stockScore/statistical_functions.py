from stockScore import start


def suite(batch_data, stock_scores):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :return: Returns an updated stock_score dictionary that runs all functions
    in statistical_functions module. Make sure to set stock_score to the function
    so that suite() can return updated stock scores.
    """
    stock_scores = p_to_b_test(batch_data, stock_scores)
    return stock_scores


def p_to_b_test(batch_data, stock_scores):
    """
    :param batch_data: List of concatenated symbols -- use get_symbols() and set_batches()
    functions to set batch_data
    :param stock_scores: Dictionary with stock symbols and corresponding scores
    (ex: {'AAPL': 5, 'FB': 7, 'TSLA': 1, 'TJX': 12}
    :return: Returns an updated stock_score dictionary. Make sure to set stock_score to the function
    so that p_to_b_test() can return updated stock scores.
    """
    stats = start.get_stats(batch_data)
    for symbol in stock_scores:
        if stats.get(symbol):
            if stats[symbol].get('stats').get('priceToBook'):
                pts = round(5 / (stats[symbol]['stats']['priceToBook'] + 0.8))
                if 0 < stats[symbol]['stats']['priceToBook'] <= 1:
                    stock_scores[symbol] += pts
                    print(symbol + " score went up by " +
                          str(pts) + "-- price to book between 0 and 1")
                elif 1 < stats[symbol]['stats']['priceToBook'] <= 2:
                    stock_scores[symbol] += pts
                    print(symbol + " score went up by " +
                          str(pts) + "-- price to book between 1 and 2")

    return stock_scores
