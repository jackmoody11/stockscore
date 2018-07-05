# Modules
from stockScore import wacc
from stockScore import start
import os

# Env Vars
av_api_key = os.environ.get('av_api_key')
in_user = os.environ.get('in_user')
in_pass = os.environ.get('in_pass')

# Base Vars
iex_url_base = "https://api.iextrading.com/1.0/"
in_url_base = "https://api.intrinio.com"
market_risk_premium = .045


symbols = start.get_symbols()

# Calculate WACC


def get_waccs(tickers):

    stock_waccs = {}
    for ticker in tickers:
        stock_waccs[ticker] = wacc.get_wacc(ticker, market_risk_premium)

    return stock_waccs


waccs = get_waccs(symbols)
print(waccs)
# Initialize variables
shareholder_equity, net_income = (0,) * 2
good_picks = []

# Loop for DCF
# for symbol in symbols:
# 	financials_json = requests.get(iex_url_base + "stock/" + symbol + "/financials").json()
# 	shareholderEquity = int(financials_json['financials'][0]['shareholderEquity'])

# 	for i in range(0,4):
# 		base = financials_json['financials'][i]
# 		net_income += int(base['netIncome'])

# 	financials = [shareholder_equity, net_income]

# curl "https://api.intrinio.com/companies?ticker=AAPL" -u "142352fdbd085ec046873f47748139e3:1289904d544b7fe0cc14e21d6622e24c"

# get financial data from IEX and set to variables
# get beta from yahoo
# get expected SGR from NASDAQ
# set appropriate TV - determine TVGR based on projected SGR
#   ~for next 5 yrs - higher SGR = higher TVGR
# Check that all variables are set - if any data is missing, don't do anything else for that stock
#   ~make a vector containing all of the stocks that didn't have enough data to run and you can create
#   ~another program later to find what values were missing
# set variables for WACC, IS, BS
# find EV by DCF
# if EV > MV, add stock name to goodPicks
# and calculate percent upside for stock and add that to goodPicksPercentUpside
