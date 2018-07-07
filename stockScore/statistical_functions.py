from stockScore import start


def suite(batch_symbols, stock_scores):

    stock_scores = p_to_b_test(batch_symbols, stock_scores)
    return stock_scores


def p_to_b_test(batch_data, stock_scores):

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
