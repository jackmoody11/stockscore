from stockScore import technical_functions as tf
from stockScore import start as start

symbols, _, batch_data = start.total_setup()
stats = start.get_stats(batch_data)


def test_moving_avg_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = tf.moving_avg_test(batch_data, scores, stats=stats)
    assert len(
        scores) >= 1000, 'At least 1000 moving avg scores listed in stock_scores dictionary'


def test_moving_avg_not_all_zero():

    scores = start.init_stock_scores(symbols)
    scores = tf.moving_avg_test(batch_data, scores, stats=stats)
    assert not all(score == 0 for score in scores.values())
