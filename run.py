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
test_date = datetime.date(2016, 1, 1)
d, r = sk.loadTrainDataByIdFixedRow('2330', test_date, 30, 7)
#print d.tolist()
#print len(d.tolist())
print sum(d.tolist(), [])
#print len(sum(d.tolist(), []))
print r

test_date = datetime.date(2016, 2, 1)
d, r = sk.loadTrainDataByIdFixedRow('2330', test_date, 30, 7)

#print d.tolist()
#print len(d.tolist())
print sum(d.tolist(), [])
#print len(sum(d.tolist(), []))
print r

exit(0)
while da < today:
    filePath = 'data/' + da.strftime("%Y%m%d") + '.csv'
    sk.convertCSV(filePath, da)
    da = da + one_day
