#!/usr/bin/env python
import datetime
from datetime import timedelta
from stock import stockImport

sk = stockImport()
sk.downloadData()
last_update = sk.loadDate()
#sk.aggregate()
#start_date = datetime.date(2016, 12, 20)
#today = datetime.date(2016, 12, 30)
#start_date = datetime.date(2009, 9, 25)
#start_date = datetime.date(2004, 2, 11)

#from last update
start_date = last_update.date()
today = datetime.date.today()
one_day = timedelta(days=1)
da = start_date
while da < today:
    filePath = 'data/' + da.strftime("%Y%m%d") + '.csv'
    sk.convertCSV(filePath, da)
    da = da + one_day
