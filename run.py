#!/usr/bin/env python
import datetime
from datetime import timedelta
from stock import stockImport

sk = stockImport()
sk.downloadData()
last_update = sk.loadDate()

#start_date = datetime.date(2016, 12, 20)
#today = datetime.date(2016, 12, 30)
#start_date = datetime.date(2009, 9, 25)
#start_date = datetime.date(2004, 2, 11)

#from last update
start_date = last_update.date()
today = datetime.date.today()
one_day = timedelta(days=1)
da = start_date

print ("update dataframe from {} to {} ".format(start_date, today))
X = []
Y = []
test_date = datetime.date(2016, 11, 1)
sk.loadTrainDataByIdFixedRow('2330', test_date, 30, 7)
test_date = datetime.date(2016, 11, 2)
sk.loadTrainDataByIdFixedRow('2330', test_date, 30, 7)
test_date = datetime.date(2016, 11, 3)
sk.loadTrainDataByIdFixedRow('2330', test_date, 30, 7)
test_date = datetime.date(2016, 11, 4)
sk.loadTrainDataByIdFixedRow('2330', test_date, 30, 7)
test_date = datetime.date(2016, 12, 10)
sk.loadTrainDataByIdFixedRow('2330', test_date, 30, 7)
exit(0)
while da < today:
    filePath = 'data/' + da.strftime("%Y%m%d") + '.csv'
    sk.convertCSV(filePath, da)
    da = da + one_day
