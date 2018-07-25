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
        self.ticker = ""
        self.company_name = ""
        self.current_price = None
        self.market_cap = None

        # Value
        self.pe_ratio = None
        self.pb_ratio = None
        self.net_income = {}
        self.dividends = {}
        self.ttm_gross_profit = None
        self.ttm_cost_of_rev = None
        self.ttm_op_rev = None
        self.ttm_total_rev = None
        self.ttm_op_income = None
        self.ttm_net_income = None
        self.ttm_r_and_d = None
        self.ttm_op_expense = None
        self.current_assets = None
        self.total_assets = None
        self.total_liabilities = None
        self.current_cash = None
        self.current_debt = None
        self.total_cash = None
        self.total_debt = None
        self.shareholder_equity = None
        self.cash_flow = None
        self.op_gains_losses = None
        self.dividend_yield = None
        self.shares_outstanding = None
        self.return_on_equity = None
        self.ebitda = None
        self.ttm_eps = None
        self.return_on_assets = None
        self.price_to_sales = None
        self.short_ratio = None
        self.profit_margin = None

        # Momentum
        self.ma_50 = None
        self.ma_200 = None
        # Not sure that these will be very useful
        self.five_year_change = None
        self.two_year_change = None
        self.one_year_change = None
        self.ytd_change = None
        self.six_month_change = None
        self.three_month_change = None
        self.one_month_change = None
        self.five_day_change = None

        # Initialize DCF variables
        self.wacc = None
        self.cost_of_equity = None
        self.cost_of_debt = None
        self.dcf_fair_value = None
