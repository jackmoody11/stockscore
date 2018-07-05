from stockScore import statistical_functions as sf
from stockScore import start as start

iex_url_base = "https://api.iextrading.com/1.0/"
symbols = start.get_symbols()
batch_symbols = start.set_batches(symbols)


def test_p_to_b_test_gets_at_least_1000_scores():
    scores = start.init_stock_scores(symbols)
    scores = sf.p_to_b_test(batch_symbols, scores)
    assert len(scores) >= 1000, 'At least 1000 scores for price/book test'


def test_p_to_b_not_all_zero():
    scores = start.init_stock_scores(symbols)
    scores = sf.p_to_b_test(batch_symbols, scores)
    assert not all(score == 0 for score in scores.values())
