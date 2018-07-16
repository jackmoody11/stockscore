# NOTE: NOT CURRENTLY IN USE - FOR FUTURE USE
# from stockScore import start as start


class Stock:

    def __init__(self):

        # Initialize different scores
        self.total_score = 0
        self.value_score = 0
        self.growth_score = 0
        self.momentum_score = 0
        self.sentiment_score = 0

        # Initialize stock info
        self.ticker = ''
        self.company_name = ''
        self.current_price = None
        self.market_cap = None

        # Value
        self.pe_ratio = None
        self.pb_ratio = None
        self.net_income = {}
        self.dividends = {}

        # Momentum
        self.ma_50 = None
        self.ma_200 = None

        # Initialize DCF variables
        self.wacc = None
        self.cost_of_equity = None
        self.cost_of_debt = None
        self.dcf_fair_value = None
