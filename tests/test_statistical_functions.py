from stockScore import statistical_functions as sf
from stockScore import start as start

symbols = start.get_symbols()
batch_data = start.set_batches(symbols)
stats = start.get_stats(batch_data)
chart = start.get_chart(batch_data)


def test_trading_volume_test_returns_scores():

    scores = start.init_stock_scores(symbols)
    scores = sf.trading_volume_test(batch_data, scores, chart=chart)
    assert len(
        scores) >= 1000, 'At least 1000 dividend scores listed in stock_scores dictionary'


def test_trading_volume_test_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = sf.trading_volume_test(batch_data, scores, chart=chart)
    assert not all(score == 0 for score in scores.values())


def test_p_to_b_test_returns_scores():
    scores = start.init_stock_scores(symbols)
    scores = sf.p_to_b_test(batch_data, scores, stats=stats)
    assert len(scores) >= 1000, 'At least 1000 scores for price/book test'


def test_p_to_b_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = sf.p_to_b_test(batch_data, scores)
    assert not all(score == 0 for score in scores.values())
