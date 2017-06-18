import os, csv, requests, sys
import pandas as pd
from bs4 import BeautifulSoup

def get_tdcc_date(stock_id):
	date_list =[]
	url = "http://www.tdcc.com.tw/smWeb/QryStock.jsp"
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	select = soup.find('select', attrs={'name':'SCA_DATE'})
	for row in select:
		for option in row:
			if option.isdigit():
				date_list.append(option)
	return date_list

def get_tdcc(stock_id, date_list):
    data = []
    for date_string in date_list:
        url = "http://www.tdcc.com.tw/smWeb/QryStock.jsp?SCA_DATE=" + date_string + "&SqlMethod=StockNo&StockNo=" + stock_id + "&StockName=&sub=%ACd%B8%DF"        
        res = requests.get(url)
        if res.status_code != 200:
        	continue;
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.findAll('table', attrs={'cellspacing':'0', 'cellpadding':'0', 'width':"100%", 'border':'1', 'class':"mt", 'bordercolor':"#B0CAFF"})
        try:
        	for row in table[1].findAll("tr"):
	            tds = row.findAll("td")
	            if tds[0].contents[0].isdigit():
	                date_data=[]
	                date_data.append("{}_{}".format(date_string, tds[1].contents[0]))
	                date_data.append(tds[2].contents[0]) 
	                date_data.append(tds[3].contents[0])
	                date_data.append(tds[4].contents[0])
	#                 print "range:", tds[1].contents[0]
	#                 print "population:", tds[2].contents[0]
	#                 print "stock number:", tds[3].contents[0]
	#                 print "portion:", tds[4].contents[0]
	#                 print "============="
	                data.append(date_data)
        except IndexError:
        	# print "this request is no data, skip"
        	break
    df_data = pd.DataFrame(data, columns=['date_level', 'population', 'stock number', 'total portion'])
    return df_data
	

def get_all_stockid(data_path): 
	stock_list = []
	for file_name in os.listdir(data_path):
		stock_id = file_name.split('.csv')[0]
		stock_list.append(stock_id)
	return stock_list


reload(sys)
sys.setdefaultencoding('utf-8')

stock_list = get_all_stockid('bystock/')
# stock_list = ['0055']

for stock_id in stock_list:
	date_list = get_tdcc_date(stock_id=stock_id)
	df_data = get_tdcc(stock_id=stock_id, date_list=date_list)
	file_name = "tdcc/{}_tdcc.csv".format(stock_id)
	df_data.to_csv(file_name, sep=',', index=False, encoding='utf-8')
	print file_name, "completed"

