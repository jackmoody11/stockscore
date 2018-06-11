import setup

iex_url_base = "https://api.iextrading.com/1.0/"


def test_get_symbols():

    assert setup.get_symbols(iex_url_base)


def test_init_stock_scores():

    symbols = setup.get_symbols(iex_url_base)
    stock_scores = setup.init_stock_scores(symbols)
    assert all(scores == 0 for scores in stock_scores.values())


def test_set_batches():

    symbols = setup.get_symbols(iex_url_base)
    assert setup.set_batches(symbols)


def test_total_setup():

    symbols, stock_scores, batch_symbols = setup.total_setup()
    assert len(symbols) >= 100, 'Symbols added'
    assert all(scores == 0 for scores in stock_scores.values()), 'All initial stock scores set to zero'
    assert len(batch_symbols) >= 2, 'At least 2 batches of stocks -- 101+ stocks used'



def test_soup_it():

    assert setup.soup_it('https://google.com')

