import setup
import openpyxl as xl
import datetime

filename = 'stock_score_data.xlsx'
wb = xl.load_workbook(filename)
ws = wb['Data']
ws['B1'] = datetime.datetime.now()
wb.save(filename)
print(ws['B1'].value)

last_updated = ws['B1'].value
time_now = datetime.datetime.now()
time_diff = time_now - last_updated
if last_updated == None ||
