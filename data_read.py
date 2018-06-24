# Modules
import openpyxl as xl
import pandas as pd
import datetime
import requests

# Variables
iex_url_base = "https://api.iextrading.com/1.0/"


# Functions
def xl_get_symbols():

    file = 'stock_score_data.xlsx'
    wb = xl.load_workbook(file)
    ws = wb['Data']
    symbols = []

    for i in range(4,6000):
        if ws['A%s'%i].value != None:
            symbols.append(ws['A%s'%i].value)
    return symbols


def get_symbols(iex_url_base = iex_url_base, manual = False):

    """Gets all symbols from IEX API (uppercase) or Excel
    if saved within last day. """

    file = 'stock_score_data.xlsx'
    wb = xl.load_workbook(file)
    ws = wb['Data']

    last_updated = ws['B1'].value
    time_now = datetime.datetime.now()
    time_diff = time_now - last_updated

    if (last_updated == None or time_diff > datetime.timedelta(days=5) or manual):

        symbols_json = requests.get(iex_url_base + "ref-data/symbols").json()
        symbols = []
        for i in range(len(symbols_json)):
            if symbols_json[i]['type'] == 'cs':
                symbols.append(symbols_json[i]['symbol'])

    else:

        symbols = xl_get_symbols()

    return symbols


def xl_update_symbols():

    file = 'stock_score_data.xlsx'
    wb = xl.load_workbook(file)
    ws = wb['Data']

    last_updated = ws['B1'].value
    time_now = datetime.datetime.now()
    time_diff = time_now - last_updated

    if (last_updated == None or time_diff > datetime.timedelta(days=5)):
        ws['B1'].value = datetime.datetime.now()
        last_updated = datetime.datetime.now()
        symbols = get_symbols(manual = True)
        for i in range(4,len(symbols)+4):
            ws['A%s'%i] = symbols[i - 4]

    wb.save(file)
    # print("The new last updated time is " + str(last_updated))
    # print(ws['A10'].value)




