#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import datetime
from datetime import timedelta
import argparse
import math

WIND=5

def filter1(data):
    del data['TO']
    del data['HP']
    del data['LP']
    del data['TC']
    total_len = len(data.index)
    #print total_len
    diff = 0
    mean5 = 0
    start_idx = 0
    stop_idx = 0
    start_dates = []
    idx = 0
    count5p = 0
    count10p = 0
    wave_max = 0
    #print data.index
    #print data['TV'].rolling(WIND).mean().shift(-WIND )
    data['tv_mean'] = data['TV'].rolling(WIND).mean().shift(1)
    for i, row in data.iterrows():
        if math.isnan(row['tv_mean']):
            idx = idx + 1
            continue
        if (row['TV'] > 2 * row['tv_mean'] and row['CR'] > 5) or row['OR'] == 10:
            if start_idx == 0 or idx - start_idx > WIND:
                start_date = i
                start_idx = idx
            last_date = i
            start_dates.append(i)
            mean5 = row['tv_mean']
            idx = idx + 1
            stop_idx = 0
            continue
        if idx - start_idx < 5 and row['TV'] > 2 * mean5:
            #same wave
            idx = idx + 1
            last_date = i
            start_dates.append(i)
            stop_idx = 0
            continue
        if start_idx > 0:
            start_idx = 0
            wave = data.loc[start_date: last_date]
            #print "wave start:"
            #print wave
            wave_max = wave['TV'].max()
            idx = idx + 1
        if row['TV'] < wave_max/2 or row['CR'] < 4 :
            if stop_idx == 0:
                #print "wave stop"
                #print i
                stop_idx = idx

    Mm = (data['CP'].max() - data['CP'].min() ) * 100/ data['CP'].min()
    return start_dates, Mm
    #print data


def preprocess(days=30, sid=None, date_from=None):
    result = []
    diff = 0
    res = pd.DataFrame(columns=('id', 'rate'))
    today = datetime.date.today()
    try:
        if date_from == "today":
            df = pd.DataFrame.from_csv('bystock/' + sid + ".csv")
            if len(df["2017-01-01":today.strftime("%Y-%m-%d")].index) == 0:
                return result, diff
        else:
            dfo = pd.DataFrame.from_csv('bystock/' + sid + ".csv")
            fdate = datetime.datetime.strptime(date_from, "%Y%m%d")
            df = dfo["20100101":fdate.strftime("%Y-%m-%d")]
            #df = dfo[]
        subset = df.tail(days + 1)
        last_cp = 0
        df_r = subset[0:0]
        df_r['YP'] = pd.Series(np.random.randn(0), index=df_r.index)
        df_f = subset[0:0]
        df_f['HR'] = pd.Series(np.random.randn(0), index=df_f.index)
        df_f['LR'] = pd.Series(np.random.randn(0), index=df_f.index)
        df_f['OR'] = pd.Series(np.random.randn(0), index=df_f.index)
        df_f['CR'] = pd.Series(np.random.randn(0), index=df_f.index)
        for idx,row in subset.iterrows():
            row['YP'] = last_cp
            df_r.loc[idx] = row
            last_cp = row['CP']
        #print df_r
        for idx,row in df_r.iterrows():
            row['HR'] = (row['HP'] - row['YP']) * 100/row['YP']
            row['LR'] = (row['LP'] - row['YP']) * 100/row['YP']
            row['OR'] = (row['OP'] - row['YP']) * 100/row['YP']
            row['CR'] = (row['CP'] - row['YP']) * 100/row['YP']
            df_f.loc[idx] = row
            #print row
        final = df_f.tail(days)
        final['TV'] = final['TV'].apply(lambda x: x/1000 )
        final['HR'] = final['HR'].apply(lambda x: float('%.2f' % x ))
        final['LR'] = final['LR'].apply(lambda x: float('%.2f' % x ))
        final['OR'] = final['OR'].apply(lambda x: float('%.2f' % x ))
        final['CR'] = final['CR'].apply(lambda x: float('%.2f' % x ))
        #final['HR'] = final.apply(lambda x: '%.2f' % x)
        result, diff = filter1(final)
        #print "https://tw.stock.yahoo.com/q/ta?s=" + sid
        #print subset 
        #print df.tail(days)
    except Exception as e:
        print e
        a = 1
    return result, diff


def main(days=30, sid=None, date_from=None):
    if sid != None:
        res, diff = preprocess(days=days, sid = sid, date_from=date_from)
    else:

        df = pd.DataFrame()
        for root, dirs, files in os.walk("./bystock"):
            path = root.split(os.sep)
            for f in files:
                stockid = f.split('.')[0]
                #print stockid
                if len(f) != 8:
                    continue
                res, diff = preprocess(days=days, sid = stockid, date_from=date_from)
                if len(res) > 0:
                    df = df.append({'stockid': stockid, 'rate': diff, 'hits': res}, ignore_index=True)
        #sdf =  df.sort(['rate'], ascending=[1])
        #print "crazy......."
        #print sdf.head(10)
        #print "warn up......."
        #print sdf.tail(10)
        print df['stockid'].to_string(index=False)


    #print res.sort(['rate'])
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--stockid", type=str, default=None,
                    help="The stock id")
    parser.add_argument("-d", "--days", type=int, default=50,
                    help="The n days")
    parser.add_argument("-f", "--fromdate", type=str, default="today",
                    help="The analyzed date string")

    args = parser.parse_args()
    main(days=args.days, sid = args.stockid, date_from=args.fromdate)
