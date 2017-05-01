#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import datetime
from datetime import timedelta
import argparse

def main(days=30, number=10):
    today = datetime.date.today()
    one_day = timedelta(days=1)
    yesterday = datetime.date.today() - one_day

    today_str = today.strftime("%Y-%m-%d")
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    start_day_str = (today - days * one_day).strftime("%Y-%m-%d")
    ystart_day_str = (today - (days +1 ) * one_day).strftime("%Y-%m-%d")
    print "from : " + start_day_str + " to : " + today_str
    #print "from : " + ystart_day_str + " to : " + yesterday_str
    res = pd.DataFrame(columns=('id', 'rate'))
    yres = pd.DataFrame(columns=('id', 'rate'))
    idx = 0
    for root, dirs, files in os.walk("./bystock"):
        path = root.split(os.sep)
        for f in files:
            stockid = f.split('.')[0]
            if len(f) != 8:
                continue

            df = pd.DataFrame.from_csv('bystock/' + f)
            try:
                fdf = df.ix[start_day_str:today_str]
                rate = (fdf['CP'][-1] - fdf['CP'][0]) / fdf['CP'][0]
                res.loc[idx] = [ stockid, rate]
                idx = idx + 1
            except Exception as e:
                #print e
                a = 1
            try:
                fdf = df.ix[ystart_day_str:yesterday_str]
                rate = (fdf['CP'][-1] - fdf['CP'][0]) / fdf['CP'][0]
                yres.loc[idx] = [ stockid, rate]
                idx = idx + 1
            except Exception as e:
                #print e
                a = 1

    final = res[np.isfinite(res['rate'])]

    yfinal = yres[np.isfinite(yres['rate'])]


    sort = final.sort_values(['rate'], ascending = False)
    print "top growth"
    tmp = sort.head(number)
    tmp['rate'] = tmp['rate'].apply(lambda x:  '%.2f' % (x * 100))
    print tmp.to_string(index=False)
    #tmp = sort.head(number).to_string(index=False)
    #print tmp
    #print tmp['rate'].apply(lambda x: x * 100 )
    
    a = sort.head(number)['id'].tolist()
    sort = final.sort_values(['rate'], ascending = True)
    print "top drop"
    tmp = sort.head(number)
    tmp['rate'] = tmp['rate'].apply(lambda x:  '%.2f' % (x * 100))
    print tmp.to_string(index=False)
    #print tmp['rate'].apply(lambda x: x * 100 )
    b = sort.head(number)['id'].tolist()

    sort = yfinal.sort_values(['rate'], ascending = False)
    #print "top growth"
    #print sort.head(number).to_string(index=False)
    A = sort.head(number)['id'].tolist()
    sort = yfinal.sort_values(['rate'], ascending = True)
    #print "top drop"
    #print sort.head(number).to_string(index=False)
    B =  sort.head(number)['id'].tolist()

    print "new in top"
    print list(set(a) - set(A))
    print "bye from top"
    print list(set(A) - set(a))

    print "new in drop"
    print list(set(b) - set(B))
    print "bye from drop"
    print list(set(B) - set(b))

    #print res.sort(['rate'])
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-d", "--days", type=int, default=30,
                    help="The past n days")
    parser.add_argument("-n", "--number", type=int, default=10,
                    help="The number of head")

    args = parser.parse_args()
    main(days=args.days, number=args.number)
