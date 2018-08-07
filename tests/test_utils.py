from stockscore import utils
symbols = utils.get_symbols()


def test_get_symbols_not_empty():

    if not utils.get_symbols():
        raise AssertionError('Returns empty list of symbols')


def test_get_symbols_contains_at_least_1000_symbols():

    if not(len(symbols) >= 1000):
        raise AssertionError('There are at least 1000 stock symbols')


def test_init_stock_scores_sets_all_scores_to_zero():

    stock_scores = utils.init_stock_scores(symbols)
    if not(all(scores == 0 for scores in stock_scores.values())):
        raise AssertionError('All scores set to zero')


def test_init_stock_scores_returns_scores():

    stock_scores = utils.init_stock_scores(symbols)
    if not(len(stock_scores) >= 1000):
        raise AssertionError('At least 1000 stock scores initialized')


def test_set_batches_not_empty():

    if not utils.set_batches(symbols):
        raise AssertionError('Batches set - list is empty')


def test_set_batches_contains_at_least_10_batches():

    batches = utils.set_batches(symbols)
    if not(len(batches) >= 10):
        raise AssertionError('At least 10 batches of symbols')


def test_total_utils():

    _, stock_scores, batch_symbols = utils.total_setup()
    if not(len(symbols) >= 100):
        raise AssertionError('Symbols not added')
    if not(all(scores == 0 for scores in stock_scores.values())):
        raise AssertionError('All initial stock scores set to zero')
    if not(len(batch_symbols) >= 10):
        raise AssertionError('Not at least 10 batches of stocks -- 1000+ stocks should be used')


def test_soup_it():

    if not utils.soup_it('https://google.com'):
        raise AssertionError('Able to fetch parsed HTML from Google')


def test_return_top_gives_correct_largest_value():

    my_family = {'Billy': 2, 'Bob': 14, 'Suzy': 7, 'Dad': 49, 'Mom': 48}
    top = utils.return_top(my_family, 5)
    if not(top[0][0] == 'Dad'):
        raise AssertionError('return_top() does not return greatest value in dictionary')


def test_return_top_assumes_length_of_dictionary_by_default():

    my_family = {'Billy': 2, 'Bob': 14, 'Suzy': 7, 'Dad': 49, 'Mom': 48}
    top = utils.return_top(my_family)
    if not(top[4][0] == 'Billy'):
        raise AssertionError('return_top() does not assume length of dictionary by default')

# These need work - Don't think these are working as planned
# *_, batch_data = utils.total_setup()
#
#
# def test_get_stats():
#
#     stats = utils.get_stats(batch_data)
#     aapl_stats = stats['AAPL']
#     assert aapl_stats, 'Successfully retrieved AAPL stats'
#
#
# def test_get_financials():
#
#     financials = utils.get_financials(batch_data)
#     aapl_financials = financials['AAPL']
#     assert aapl_financials, 'Successfully retrieved AAPL financials'
#
#
# def test_get_chart():
#
#     chart = utils.get_chart(batch_data)
#     aapl_chart = chart['AAPL']
#     assert aapl_chart, 'Successfully retrieved AAPL chart'
#
#
# # AAPL will work for now, but this may need to be revisited if AAPL doesn't split in future
# def test_get_splits():
#
#     splits = utils.get_splits(batch_data)
#     aapl_splits = splits['AAPL']
#     assert aapl_splits, 'Successfully retrieved AAPL spl
