from autoDCF import wacc as wacc


def test_get_beta():

    if wacc.get_beta('aapl') is None:
        raise AssertionError('Beta not received when symbol lowercase')
    if wacc.get_beta('Aapl') is None:
        raise AssertionError('Beta not received when symbols mixed case')
    if wacc.get_beta('AAPL') is None:
        raise AssertionError('Beta not received when symbols upper case')
