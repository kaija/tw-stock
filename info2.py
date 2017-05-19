#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import datetime
from datetime import timedelta
import argparse
import os.path

def main(days=30, sid=None):

    res = pd.DataFrame(columns=('id', 'rate'))
    try:
        if os.path.isfile('bystock/' + sid + ".csv"):
            df = pd.DataFrame.from_csv('bystock/' + sid + ".csv")
        else:
            df = pd.DataFrame.from_csv('byemg/' + sid + ".csv")

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
        final['TV'] = final['TV'].apply(lambda x: int(x/1000) )
        final['HR'] = final['HR'].apply(lambda x: '%.2f' % x )
        final['LR'] = final['LR'].apply(lambda x: '%.2f' % x )
        final['OR'] = final['OR'].apply(lambda x: '%.2f' % x )
        final['CR'] = final['CR'].apply(lambda x: '%.2f' % x )
        #final['HR'] = final.apply(lambda x: '%.2f' % x)
        del final['HP']
        del final['LP']
        del final['DF']
        del final['RD']
        del final['TC']
        del final['OR']
        del final['TO']
        print final
        #print subset 
        
        #print df.tail(days)
    except Exception as e:
        print e
        a = 1


    #print res.sort(['rate'])
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--stockid", type=str, default="",
                    help="The stock id")
    parser.add_argument("-d", "--days", type=int, default=10,
                    help="The n days")

    args = parser.parse_args()
    main(days=args.days, sid = args.stockid)
