import setup

iex_url_base = "https://api.iextrading.com/1.0/"
symbols = setup.get_symbols(iex_url_base)


def test_get_symbols():
    assert setup.get_symbols(iex_url_base)


def test_init_stock_scores():
    stock_scores = setup.init_stock_scores(symbols)
    assert all(value == 0 for value in stock_scores.values())

def test_set_batches():
    assert setup.set_batches(symbols)


def test_soup_it():
    assert setup.soup_it('https://google.com')

