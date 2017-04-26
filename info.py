#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import datetime
from datetime import timedelta
import argparse

def main(days=30, sid=None):

    res = pd.DataFrame(columns=('id', 'rate'))
    try:
        df = pd.DataFrame.from_csv('bystock/' + sid + ".csv")
        print df.tail(days)
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
