import stockScore.wacc as wacc


def test_get_beta():

    iex_url_base = "https://api.iextrading.com/1.0/"
    assert wacc.get_beta('aapl') is not None, 'Beta received with lowercase'
    assert wacc.get_beta('Aapl') is not None, 'Beta received with mixed case'
    assert wacc.get_beta('AAPL') is not None, 'Beta received with upper case'
