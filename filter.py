#!/usr/bin/env python
import pandas as pd

def f1(x):
    print x
    return 1
    

res = pd.DataFrame(columns=('id', 'rate'))
try:
    df = pd.DataFrame.from_csv('bystock/2439.csv')
    df['DF'].rolling(3).apply(lambda x: f1(x))
except Exception as e:
    print e
