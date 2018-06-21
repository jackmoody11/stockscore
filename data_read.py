import setup
import openpyxl as xl
import datetime

filename = 'stock_score_data.xlsx'
wb = xl.load_workbook(filename)
ws = wb['Data']

last_updated = ws['B1'].value
time_now = datetime.datetime.now()
time_diff = time_now - last_updated

day_in_seconds = 86400
if (last_updated == None or time_diff.total_seconds() >= day_in_seconds):
    last_updated = datetime.datetime.now()
    wb.save(filename)
print("The new last updated time is " + str(last_updated))
