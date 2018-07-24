import numpy as np
import os
import requests
from stockScore import start

iex_url_base = "https://api.iextrading.com/1.0/"
in_url_base = "https://api.intrinio.com"
in_user = os.environ.get('in_user')
in_pass = os.environ.get('in_pass')


def get_beta(symbol):

    json = requests.get(iex_url_base + '/stock/' + symbol.lower() + '/stats').json()
    if float(json['beta']):
        beta = float(json['beta'])
    else:
        beta = None
    return beta


def get_debt_to_equity(symbol):

    de_json = requests.get(f'{iex_url_base}stock/{symbol.lower()}/financials').json()
    try:
        total_debt = int(de_json['financials'][0]['totalDebt'])
        total_equity = int(de_json['financials'][0]['shareholderEquity'])
        debt_to_equity = total_debt / total_equity
    except (KeyError, TypeError):
        debt_to_equity = None

    return debt_to_equity


def get_rf():

    rf_url = 'https://fred.stlouisfed.org/series/DGS30'
    rf_soup = start.soup_it(rf_url)
    if float(rf_soup.find('span', attrs={'class': 'series-meta-observation-value'}).text.strip()):
        rf_rate = float(rf_soup.find(
            'span', attrs={'class': 'series-meta-observation-value'}).text.strip())
        return rf_rate / 100
    return None


def get_tax_rate_iex(symbol):

    json = requests.get(iex_url_base + 'stock/' +
                        symbol.lower() + '/financials').json()
    tax_rates = []
    for i in range(0, 4):
        op_income = int(json['financials'][i]['operatingIncome'])
        net_income = int(json['financials'][i]['netIncome'])
        taxes = op_income - net_income
        tax_rate = taxes / op_income
        tax_rates.append(tax_rate)
    # Use numpy to get average tax rate for trailing twelve months
    return np.mean(tax_rates)


def get_tax_rate(symbol):

    in_json = requests.get(f'{in_url_base}/financials/standardized?identifier={symbol.upper()}\
                           &statement=income_statement&fiscal_year=2017&fiscal_period=FY',
                           auth=(in_user, in_pass)).json()
    pretax_income = in_json['data'][11]['value']
    taxes = in_json['data'][12]['value']
    tax_rate = taxes / pretax_income
    return tax_rate


def get_interest_exp(symbol):

    in_json = requests.get(f'{in_url_base}/financials/standardized?identifier={symbol.upper()}\
                           &statement=income_statement&fiscal_year=2017&fiscal_period=FY',
                           auth=(in_user, in_pass)).json()
    data = in_json['data']
    int_exp_dict = next((item for item in data if item['xbrl_tag'] == 'InterestExpense'), None)
    if int_exp_dict:
        interest_expense = int_exp_dict['value']
    else:
        # Will need to find another way to get interest expense if not
        # available
        interest_expense = 0.05
    return interest_expense


# def getPretaxIncome(symbol):

def get_wacc(symbol, rp):

    debt_to_equity = get_debt_to_equity(symbol)
    beta = get_beta(symbol)
    risk_free = get_rf()
    e_to_v = 1 / (1 + debt_to_equity)
    d_to_v = 1 / (1 + (1 / debt_to_equity))
    cost_of_equity = risk_free + beta * rp
    tax_rate = get_tax_rate(symbol)
    wacc = (e_to_v * cost_of_equity) + (d_to_v * (1 - tax_rate) * get_interest_exp(symbol))  # /getPretaxIncome(symbol)

    return wacc
