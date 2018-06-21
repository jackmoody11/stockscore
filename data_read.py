import openpyxl as xl
import pandas as pd
import datetime

file = 'stock_score_data.xlsx'
wb = xl.load_workbook(file)
ws = wb['Data']

last_updated = ws['B1'].value
time_now = datetime.datetime.now()
time_diff = time_now - last_updated

if (last_updated == None or time_diff > datetime.timedelta(days=1)):
    last_updated = datetime.datetime.now()
    wb.save(file)
print("The new last updated time is " + str(last_updated))


def check_for_xl_symbols():
    # Check to see if Excel has symbols
    # if Excel has symbols:
    # return true
    # else
    # return false

def get_xl_symbols():
    # return array of symbols from Excel
    # Note - should only be used if symbols are in Excel
