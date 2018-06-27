# NOTE: NOT CURRENTLY IN USE - FOR FUTURE USE

import requests

class Stock:

    iex_url_base = "https://api.iextrading.com/1.0/"

    def __init__(self):

        # Initialize different scores
        self.total_score = 0
        self.value_score = 0
        self.growth_score = 0
        self.momentum_score = 0
        self.sentiment_score = 0

        # Initialize different stock attributes
        self.ticker =''
        self.company_name = ''
        self.current_price = None
        self.pe_ratio = None
        self.pb_ratio = None
        self.market_cap = None

        # Initialize DCF variables
        self.wacc = None
        self.cost_of_equity = None
        self.cost_of_debt = None
        self.dcf_fair_value = None
