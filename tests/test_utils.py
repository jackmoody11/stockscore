from stockscore import utils

symbols = utils.get_symbols()


def test_get_symbols_not_empty():

    if not utils.get_symbols():
        raise AssertionError("Returns empty list of symbols")


def test_get_symbols_contains_at_least_1000_symbols():

    if not (len(symbols) >= 1000):
        raise AssertionError("There are at least 1000 stock symbols")


def test_init_stock_scores_sets_all_scores_to_zero():

    stock_scores = utils.init_stock_scores(symbols)
    if not (
        all(
            stock_scores.loc[symbol]["Score"] == 0
            for symbol, _ in stock_scores.iterrows()
        )
    ):
        raise AssertionError("All scores set to zero")


def test_init_stock_scores_returns_scores():

    stock_scores = utils.init_stock_scores(symbols)
    if not (len(stock_scores) >= 1000):
        raise AssertionError("At least 1000 stock scores initialized")


def test_set_batches_not_empty():

    if not utils.set_batches(symbols):
        raise AssertionError("Batches set - list is empty")


def test_set_batches_contains_at_least_10_batches():

    batches = utils.set_batches(symbols)
    if not (len(batches) >= 10):
        raise AssertionError("At least 10 batches of symbols")


def test_total_utils():

    _, stock_scores, batch_symbols = utils.total_setup()
    if not (len(symbols) >= 100):
        raise AssertionError("Symbols not added")
    if not (
        all(
            stock_scores.loc[symbol]["Score"] == 0
            for symbol, _ in stock_scores.iterrows()
        )
    ):
        raise AssertionError("All initial stock scores set to zero")
    if not (len(batch_symbols) >= 10):
        raise AssertionError(
            "Not at least 10 batches of stocks -- 1000+ stocks should be used"
        )


def test_soup_it():

    if not utils.soup_it("https://google.com"):
        raise AssertionError("Able to fetch parsed HTML from Google")


# Need to add tests for checking data retrieval (stats, financials, volume, etc.)
