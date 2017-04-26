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
    today_str = today.strftime("%Y-%m-%d")
    start_day_str = (today - days * one_day).strftime("%Y-%m-%d")

    res = pd.DataFrame(columns=('id', 'rate'))
    idx = 0
    for root, dirs, files in os.walk("./bystock"):
        path = root.split(os.sep)
        for f in files:
            stockid = f.split('.')[0]
            df = pd.DataFrame.from_csv('bystock/' + f)
            try:
                
                fdf = df.ix[start_day_str:today_str]
                rate = (fdf['CP'][-1] - fdf['CP'][0]) / fdf['CP'][0]
                res.loc[idx] = [ stockid, rate]
                idx = idx + 1
            except Exception as e:
                #print e
                a = 1

    final = res[np.isfinite(res['rate'])]
    sort = final.sort_values(['rate'], ascending = False)
    print "top growth"
    print sort.head(number).to_string(index=False)

    sort = final.sort_values(['rate'], ascending = True)

    print "top drop"
    print sort.head(number).to_string(index=False)

    #print res.sort(['rate'])
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-d", "--days", type=int, default=30,
                    help="The past n days")
    parser.add_argument("-n", "--number", type=int, default=10,
                    help="The number of head")

    args = parser.parse_args()
    main(days=args.days, number=args.number)
