from stockScore import start
iex_url_base = "https://api.iextrading.com/1.0/"


def suite(batch_symbols, stock_scores):

    stock_scores = moving_avg_test(batch_symbols, stock_scores)
    return stock_scores


def moving_avg_test(batch_data, stock_scores):

    """ The Moving Avg test aims to find stocks that are gaining momentum by recognizing when the
    the 50 day moving avg is just beginning to pass the 200 day moving avg. """
    pool_outputs = start.get_pool_response(batch_data, "&types=stats")
    for first in pool_outputs:
        for batch in first:
            for ma_json in batch:
                for symbol in ma_json:
                    base = ma_json[symbol]['stats']
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
