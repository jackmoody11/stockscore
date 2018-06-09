import setup

 
def test_numbers_3_4():
    iex_url_base = "https://api.iextrading.com/1.0/"
    assert setup.get_symbols(iex_url_base)
 
def test_strings_a_3():
    assert 'a' * 3 == 'aaa' 