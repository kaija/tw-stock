import datetime
import httplib
import urllib
import os.path
import csv
import time
from datetime import timedelta
import pandas as pd
import numpy as np

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def totimestamp(dt, epoch=datetime.date(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6 

class stockImport(object):
    def __init__(self
                 ):
        print ('setup stock importer')
    def saveDate(self, date=None):
        date_str = date.strftime("%m/%d/%Y")
        print('{} finished'.format(date_str))
        f = open('./twstock.tmp', 'w')
        f.write(date_str)

    def loadDate(self):
        try:
            f = open('./twstock.tmp', 'r')
            date_str = f.readline()
            #default set to 4 PM
            return datetime.datetime.strptime(date_str + " 16:00:00", "%m/%d/%Y %H:%M:%S")
        except IOError:
            return datetime.datetime.strptime("1/1/2010 16:00:00", "%m/%d/%Y %H:%M:%S")

    def downloadData(self):
        start_day = datetime.date(2004, 2, 11);
        today = datetime.date.today()
        one_day = timedelta(days=1)
        print "start download missing data"
        print "checking from " + start_day.strftime("%Y-%m-%d") + " to " + today.strftime("%Y-%m-%d")
        download_date = start_day
        while download_date < today:
            file_name = "data/" + download_date.strftime("%Y%m%d") + ".csv"
            if os.path.isfile(file_name):
                download_date += one_day
                continue
            httpreq = httplib.HTTPConnection('www.twse.com.tw')
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            date_str = str(download_date.year - 1911 ) + download_date.strftime("/%m/%d")
            form = urllib.urlencode({'download': 'csv', 'qdate': date_str, 'selectType': 'ALLBUT0999'})
            httpreq.request("POST", "/ch/trading/exchange/MI_INDEX/MI_INDEX.php", form, headers);
            httpres =  httpreq.getresponse()
            stock_csv =  httpres.read()
            print "downloading " + file_name
            f = open(file_name, "w")
            f.write(stock_csv)
            download_date += one_day

    def insertToStock(self, stockid, row, date):
        try:
            date_str = date.strftime("%Y-%m-%d")
            df = pd.DataFrame.from_csv('bystock/' + stockid + '.csv')
            #check if there is a key
            df.loc[date_str].count()
            #key already exist. skip it   
        except KeyError:
            #no such key. insert it
            df = pd.concat([df, row])
            df.to_csv('bystock/' + stockid + '.csv')
            #print df
        except IOError:
            print('stock id: {} not exist'.format(stockid))
            row.to_csv('bystock/' + stockid + '.csv')

    def convertCSV(self, file_path=None, date=None):
        print('convert csv {}'.format(file_path))
        with open(file_path, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                if len(row) < 16:
                    #abnormal some column missing?
                    continue
                if len(row) == 17:
                    #abnormal should not more than 16 column
                    print(row)
                if len(row) == 16:
                    stockid=row[0].replace('=', '')
                    stockid=stockid.replace('"', '')
                    stockid=stockid.strip()
                    if not row[2].isdigit():
                        #skip column title
                        continue
                    TV=int(row[2])
                    TC=int(row[3])
                    TO=int(row[4])
                    RD=row[9]
                    if RD == '+':
                        DF=float(row[10])
                        RD=1
                    elif RD == '-':
                        DF=0-float(row[10])
                        RD=-1
                    else:
                        DF=0
                        RD=0
                    
                    PE=float(row[15])
                    try:
                        OP=float(row[5])
                        CP=float(row[8])
                        HP=float(row[6])
                        LP=float(row[7])
                    except ValueError:
                        OP=None
                        CP=None
                        HP=None
                        LP=None
                    #print(stockid)
                    #print('OP:{}\nCP:{}\nHP:{}\nLP:{}\nDF:{}\nRD:{}\nTV:{}\nTC:{}\nTO:{}\n'.format( OP, CP, HP, LP, DF, RD, TV, TC, TO))
                    cols = ['OP', 'CP', 'HP', 'LP', 'DF', 'RD', 'TV', 'TC', 'TO']
                    date_index = pd.date_range(date.strftime("%m/%d/%Y"), periods=1)
                    df1 = pd.DataFrame([[OP, CP, HP, LP, DF, RD, TV, TC, TO]], columns=cols)
                    df1['date'] = date_index
                    df1 = df1.set_index(['date'])
                    self.insertToStock(stockid, df1, date)
        self.saveDate(date)

