from stockScore import start


def test_get_symbols():

    assert start.get_symbols(), 'Returns non-empty list of symbols'


def test_init_stock_scores_sets_all_scores_to_zero():

    symbols = start.get_symbols()
    stock_scores = start.init_stock_scores(symbols)
    assert all(scores == 0 for scores in stock_scores.values()), 'All scores set to 0'


def test_init_stock_scores_returns_scores():

    symbols = start.get_symbols()
    stock_scores = start.init_stock_scores(symbols)
    assert len(stock_scores) >= 1000, 'At least 1000 stock scores initialized'


def test_set_batches():

    symbols = start.get_symbols()
    assert start.set_batches(symbols), 'Batches set - list is not empty'


def test_total_start():

    symbols, stock_scores, batch_symbols = start.total_setup()
    assert len(symbols) >= 100, 'Symbols added'
    assert all(scores == 0 for scores in stock_scores.values()), 'All initial stock scores set to zero'
    assert len(batch_symbols) >= 2, 'At least 2 batches of stocks -- 101+ stocks used'


def test_soup_it():

    assert start.soup_it('https://google.com'), 'Able to fetch parsed HTML from Google'


def test_return_top_gives_correct_largest_value():

    my_family = {'Billy': 2, 'Bob': 14, 'Suzy': 7, 'Dad': 49, 'Mom': 48}
    top = start.return_top(my_family, 5)
    assert top[0][0] == 'Dad', 'return_top() returns greatest value in dictionary'


def test_return_top_assumes_length_of_dictionary_by_default():

    my_family = {'Billy': 2, 'Bob': 14, 'Suzy': 7, 'Dad': 49, 'Mom': 48}
    top = start.return_top(my_family)
    assert top[4][0] == 'Billy'


# Needs work - Don't think this is working as it should
def test_get_stats():

    *_, batch_data = start.total_setup()
    stats = start.get_stats(batch_data)
    assert stats


# Needs work - Don't think this is working as it should
def test_get_financials():

    *_, batch_data = start.total_setup()
    financials = start.get_financials(batch_data)
    assert financials
