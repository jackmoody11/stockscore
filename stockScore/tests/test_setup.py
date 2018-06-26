import setup
import data_read as dr


def test_get_symbols():

    assert dr.get_symbols()


def test_init_stock_scores():

    symbols = setup.get_symbols()
    stock_scores = setup.init_stock_scores(symbols)
    assert all(scores == 0 for scores in stock_scores.values())


def test_set_batches():

    symbols = setup.get_symbols()
    assert setup.set_batches(symbols)


def test_total_setup():

    symbols, stock_scores, batch_symbols = setup.total_setup()
    assert len(symbols) >= 100, 'Symbols added'
    assert all(scores == 0 for scores in stock_scores.values()), 'All initial stock scores set to zero'
    assert len(batch_symbols) >= 2, 'At least 2 batches of stocks -- 101+ stocks used'


def test_soup_it():

    assert setup.soup_it('https://google.com')


def test_return_top_gives_correct_largest_value():

    my_family = {'Jack': 20, 'Nat': 14, 'Sam': 17, 'Dad': 49, 'Mom': 48}
    top = setup.return_top(my_family,5)
    assert top[0][0] == 'Dad'

def test_return_top_assumes_length_of_dictionary_by_default():

    my_family = {'Jack': 20, 'Nat': 14, 'Sam': 17, 'Dad': 49, 'Mom': 48}
    top = setup.return_top(my_family)
    assert top[4][0] == 'Nat'
